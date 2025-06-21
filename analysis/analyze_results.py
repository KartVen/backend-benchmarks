import os
import glob
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import gc
import numpy as np
import time

languages = {
    'csharp': 'C#',
    'java': 'Java',
    'python': 'Python',
    'php': 'PHP'
}
vus_list = [10, 20, 50, 100, 200, 500, 1000, 2000]
duration_per_vus = {
    10: 30,
    20: 25,
    50: 20,
    100: 15,
    200: 10,
    500: 10,
    1000: 5,
    2000: 5,
    5000: 5
}

base_metrics_dir = r'/media/kartven/Backup Drive/spec/metrics'
base_cpu_mem_dir = r'/media/kartven/Backup Drive/spec/cpu_mem'

def main(endpoint, endpoint_label, new_analyse=True, new_summary=True, new_plots=True):
    s_time = time.time()
    output_dir = f'./reports/{endpoint}'
    os.makedirs(output_dir, exist_ok=True)
    temp_dir = os.path.join(output_dir, '.temp')
    os.makedirs(temp_dir, exist_ok=True)

    # def filter_3sigma(arr):
    #     s = pd.Series(arr)
    #     mean, std = s.mean(), s.std()
    #     return s[(s >= mean - 3*std) & (s <= mean + 3*std)].tolist()

    def filter_3sigma(arr):
        arr_np = np.asarray(arr)
        mean = arr_np.mean()
        std = arr_np.std()
        return arr_np[(arr_np >= mean - 3 * std) & (arr_np <= mean + 3 * std)].tolist()

    def load_latency_metrics(lang, vus, duration):
        files = glob.glob(os.path.join(base_metrics_dir, lang, f'{endpoint}_{vus}_{duration}_step_*.csv'))
        latency_vals, fails_vals = [], []
        for f in files:
            for chunk in pd.read_csv(f, usecols=['metric_name', 'metric_value'], chunksize=1_000_000, low_memory=False):
                latency_vals.extend(chunk.loc[chunk['metric_name'] == 'http_req_duration', 'metric_value'].values)
        return latency_vals

    def load_waiting_metrics(lang, vus, duration):
        files = glob.glob(os.path.join(base_metrics_dir, lang, f'{endpoint}_{vus}_{duration}_step_*.csv'))
        waiting_vals, fails_vals = [], []
        for f in files:
            for chunk in pd.read_csv(f, usecols=['metric_name', 'metric_value'], chunksize=1_000_000, low_memory=False):
                waiting_vals.extend(chunk.loc[chunk['metric_name'] == 'http_req_waiting', 'metric_value'].values)
        return waiting_vals

    def load_summary_rps_metrics(lang, vus, duration):
        files = glob.glob(os.path.join(base_metrics_dir, lang, f'{endpoint}_{vus}_{duration}_summary_step_*.json'))
        rps_values = []
        for f in files:
            with open(f, 'r') as jf:
                data = json.load(jf)
                rps_values.append(data['metrics']['http_reqs']['rate'])
        return rps_values

    def load_summary_fails_metrics(lang, vus, duration):
        files = glob.glob(os.path.join(base_metrics_dir, lang, f'{endpoint}_{vus}_{duration}_summary_step_*.json'))
        fails_values = []
        for f in files:
            with open(f, 'r') as jf:
                data = json.load(jf)
                if endpoint in ['error', 'fibonacci_error']:
                    fails_values.append(data['metrics']['http_req_failed']['fails'])  # not is error
                else:
                    fails_values.append(data['metrics']['http_req_failed']['passes'])  # is error
        return [np.mean(fails_values)]

    def parse_mem_usage(mem_usage_str):
        used, total = mem_usage_str.split('/')
        used = used.strip()
        def to_mb(value):
            if 'MiB' in value:
                return float(value.replace('MiB',''))
            elif 'GiB' in value:
                return float(value.replace('GiB','')) * 1024
            else:
                return float(value)
        return to_mb(used)

    def load_cpu_percent(lang, vus, duration):
        pattern = os.path.join(base_cpu_mem_dir, lang, f'cpu_mem_{lang}_{endpoint}_{vus}_{duration}_step_*.csv')
        files = glob.glob(pattern)
        cpu_vals = []
        for f in files:
            df = pd.read_csv(f, low_memory=False)
            df['cpu%'] = df['cpu%'].str.rstrip('%').astype(float)
            cpu_vals.extend(df['cpu%'].tolist())
        return cpu_vals

    def load_mem_usage(lang, vus, duration):
        pattern = os.path.join(base_cpu_mem_dir, lang, f'cpu_mem_{lang}_{endpoint}_{vus}_{duration}_step_*.csv')
        files = glob.glob(pattern)
        mem_vals = []
        for f in files:
            df = pd.read_csv(f, low_memory=False)
            df['mem_mb'] = df['mem_usage'].map(parse_mem_usage)
            mem_vals.extend(df['mem_mb'].tolist())
        return mem_vals

    def load_mem_percent(lang, vus, duration):
        pattern = os.path.join(base_cpu_mem_dir, lang, f'cpu_mem_{lang}_{endpoint}_{vus}_{duration}_step_*.csv')
        files = glob.glob(pattern)
        mem_vals = []
        for f in files:
            df = pd.read_csv(f, low_memory=False)
            df['mem_pct'] = df['mem%'].str.rstrip('%').astype(float)
            mem_vals.extend(df['mem_pct'].tolist())
        return mem_vals

    def append_to_csv(df, filename):
        if os.path.exists(filename):
            df.to_csv(filename, mode='a', header=False, index=False)
        else:
            df.to_csv(filename, index=False)

    def save_boxplot(df, x_col, y_col, hue_col, title, ylabel, filename, facet_col=None):
        plt.figure(figsize=(12,7))
        if facet_col:
            g = sns.catplot(data=df, x=x_col, y=y_col, hue=hue_col, col=facet_col,
                            kind='box', height=5, aspect=1)
            g.set_axis_labels(x_col.capitalize(), ylabel)
            g.set_titles("{col_name}")
            g.fig.suptitle(title, y=1.05)
            plt.tight_layout()
            g.savefig(filename)
            plt.close()
        else:
            ax = sns.boxplot(data=df, x=x_col, y=y_col, hue=hue_col)
            handles, labels = ax.get_legend_handles_labels()
            labels_pl = [languages.get(label, label) for label in labels]
            ax.legend(handles, labels_pl, title=hue_col.capitalize())
            plt.title(title)
            plt.xlabel(x_col.capitalize())
            plt.ylabel(ylabel)
            plt.grid(True, linestyle='--', alpha=0.6)
            plt.tight_layout()
            plt.savefig(filename)
            plt.close()

    def save_lineplot(df, x_col, y_col, hue_col, title, ylabel, filename):
        plt.figure(figsize=(12,7))
        ax = sns.lineplot(data=df, x=x_col, y=y_col, hue=hue_col, marker='o')
        handles, labels = ax.get_legend_handles_labels()
        labels_pl = [languages.get(label, label) for label in labels]
        ax.legend(handles, labels_pl, title=hue_col.capitalize())
        plt.title(title)
        # ax.set_xticks(vus_list)
        # ax.get_xaxis().set_major_formatter(plt.ScalarFormatter())
        plt.xlabel(x_col.capitalize())
        plt.ylabel(ylabel)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.savefig(filename)
        plt.close()

    def save_lineplot_with_minmax(df, x_col, y_col, hue_col, title, ylabel, filename):
        plt.figure(figsize=(12,7))
        for key, group in df.groupby(hue_col, observed=True):
            grouped = group.groupby(x_col)[y_col].agg(['min', 'max', 'mean']).reset_index()
            plt.plot(grouped[x_col], grouped['mean'], label=languages.get(key, key))
            plt.fill_between(grouped[x_col], grouped['min'], grouped['max'], alpha=0.2)
        plt.title(title)
        plt.xlabel(x_col.capitalize())
        plt.ylabel(ylabel)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend(title=hue_col.capitalize())
        plt.tight_layout()
        plt.savefig(filename)
        plt.close()

    def process_new_analyse():
        for file in glob.glob(os.path.join(temp_dir, '*.csv')):
            os.remove(file)

        for lang_key in languages.keys():
            for vus in vus_list:
                duration = duration_per_vus[vus]
                print(f"--- Analysing {lang_key} [{endpoint} | {vus} VUs | {duration}s] ---")

                latency_raw_vals = load_latency_metrics(lang_key, vus, duration)
                print(f"Loaded: {len(latency_raw_vals)} raw latency rows")
                if latency_raw_vals:
                    latency_raw_df = pd.DataFrame({'language': [lang_key]*len(latency_raw_vals), 'vus': [vus]*len(latency_raw_vals), 'latency': latency_raw_vals})
                    append_to_csv(latency_raw_df, os.path.join(temp_dir, 'latency_raw.csv'))
                    latency_filtered_vals = filter_3sigma(latency_raw_vals)
                    del latency_raw_vals
                    print(f"Loaded: {len(latency_filtered_vals)} filtered latency rows")
                    if latency_filtered_vals:
                        latency_filtered_df = pd.DataFrame({'language': [lang_key]*len(latency_filtered_vals), 'vus': [vus]*len(latency_filtered_vals), 'latency': latency_filtered_vals})
                        del latency_filtered_vals
                        append_to_csv(latency_filtered_df, os.path.join(temp_dir, 'latency_filtered.csv'))
                gc.collect()

                waiting_raw_vals = load_waiting_metrics(lang_key, vus, duration)
                print(f"Loaded: {len(waiting_raw_vals)} raw waiting rows")
                if waiting_raw_vals:
                    waiting_raw_df = pd.DataFrame({'language': [lang_key] * len(waiting_raw_vals), 'vus': [vus] * len(waiting_raw_vals), 'waiting': waiting_raw_vals})
                    append_to_csv(waiting_raw_df, os.path.join(temp_dir, 'waiting_raw.csv'))
                    waiting_filtered_vals = filter_3sigma(waiting_raw_vals)
                    del waiting_raw_vals
                    print(f"Loaded: {len(waiting_filtered_vals)} filtered waiting rows")
                    if waiting_filtered_vals:
                        waiting_filtered_df = pd.DataFrame({'language': [lang_key] * len(waiting_filtered_vals), 'vus': [vus] * len(waiting_filtered_vals), 'waiting': waiting_filtered_vals})
                        del waiting_filtered_vals
                        append_to_csv(waiting_filtered_df, os.path.join(temp_dir, 'waiting_filtered.csv'))
                gc.collect()

                rps_vals = load_summary_rps_metrics(lang_key, vus, duration)
                print(f"Loaded RPS: {len(rps_vals)} raw rows")
                if rps_vals:
                    rps_df = pd.DataFrame({'language': [lang_key]*len(rps_vals), 'vus': [vus]*len(rps_vals), 'rps': rps_vals})
                    append_to_csv(rps_df, os.path.join(temp_dir, 'rps_raw.csv'))
                    rps_filtered_vals = filter_3sigma(rps_vals)
                    del rps_vals
                    print(f"Loaded RPS: {len(rps_filtered_vals)} filtered rows")
                    if rps_filtered_vals:
                        rps_filtered_df = pd.DataFrame({'language': [lang_key]*len(rps_filtered_vals), 'vus': [vus]*len(rps_filtered_vals), 'rps': rps_filtered_vals})
                        del rps_filtered_vals
                        append_to_csv(rps_filtered_df, os.path.join(temp_dir, 'rps_filtered.csv'))
                gc.collect()

                fails_avg_vals = load_summary_fails_metrics(lang_key, vus, duration)
                print(f"Loaded Fails: {len(fails_avg_vals)}({sum(fails_avg_vals)}) rows")
                if fails_avg_vals:
                    fails_df = pd.DataFrame({'language': [lang_key]*len(fails_avg_vals), 'vus': [vus]*len(fails_avg_vals), 'fails': fails_avg_vals})
                    del fails_avg_vals
                    append_to_csv(fails_df, os.path.join(temp_dir, 'fails.csv'))
                gc.collect()

                cpu_raw_vals = load_cpu_percent(lang_key, vus, duration)
                print(f"Loaded CPU%: {len(cpu_raw_vals)} raw rows")
                if cpu_raw_vals:
                    cpu_raw_df = pd.DataFrame({'language': [lang_key] * len(cpu_raw_vals), 'vus': [vus] * len(cpu_raw_vals), 'cpu': cpu_raw_vals})
                    append_to_csv(cpu_raw_df, os.path.join(temp_dir, 'cpu_perc_raw.csv'))
                    cpu_filtered_vals = filter_3sigma(cpu_raw_vals)
                    del cpu_raw_vals
                    print(f"Loaded CPU%: {len(cpu_filtered_vals)} filtered rows")
                    if cpu_filtered_vals:
                        cpu_filtered_df = pd.DataFrame({'language': [lang_key] * len(cpu_filtered_vals), 'vus': [vus] * len(cpu_filtered_vals), 'cpu': cpu_filtered_vals})
                        del cpu_filtered_vals
                        append_to_csv(cpu_filtered_df, os.path.join(temp_dir, 'cpu_perc_filtered.csv'))
                gc.collect()

                mem_raw_vals = load_mem_usage(lang_key, vus, duration)
                print(f"Loaded MEM_MB: {len(mem_raw_vals)} raw rows")
                if mem_raw_vals:
                    mem_raw_df = pd.DataFrame({'language': [lang_key]*len(mem_raw_vals), 'vus': [vus] * len(mem_raw_vals), 'mem': mem_raw_vals})
                    append_to_csv(mem_raw_df, os.path.join(temp_dir, 'mem_mb_raw.csv'))
                    mem_filtered_vals = filter_3sigma(mem_raw_vals)
                    del mem_raw_vals
                    print(f"Loaded MEM_MB: {len(mem_filtered_vals)} filtered rows")
                    if mem_filtered_vals:
                        mem_filtered_df = pd.DataFrame({'language': [lang_key]*len(mem_filtered_vals), 'vus': [vus] * len(mem_filtered_vals), 'mem': mem_filtered_vals})
                        del mem_filtered_vals
                        append_to_csv(mem_filtered_df, os.path.join(temp_dir, 'mem_mb_filtered.csv'))
                gc.collect()

                mem_raw_perc_vals = load_mem_percent(lang_key, vus, duration)
                print(f"Loaded MEM%: {len(mem_raw_perc_vals)} raw rows")
                if mem_raw_perc_vals:
                    mem_raw_df = pd.DataFrame({'language': [lang_key]*len(mem_raw_perc_vals), 'vus': [vus] * len(mem_raw_perc_vals), 'mem': mem_raw_perc_vals})
                    append_to_csv(mem_raw_df, os.path.join(temp_dir, 'mem_perc_raw.csv'))
                    mem_filtered_perc_vals = filter_3sigma(mem_raw_perc_vals)
                    del mem_raw_perc_vals
                    print(f"Loaded MEM%: {len(mem_filtered_perc_vals)} filtered rows")
                    if mem_filtered_perc_vals:
                        mem_filtered_df = pd.DataFrame({'language': [lang_key]*len(mem_filtered_perc_vals), 'vus': [vus] * len(mem_filtered_perc_vals), 'mem': mem_filtered_perc_vals})
                        del mem_filtered_perc_vals
                        append_to_csv(mem_filtered_df, os.path.join(temp_dir, 'mem_perc_filtered.csv'))
                gc.collect()

    def generate_summary_tables():
        for file in glob.glob(os.path.join(output_dir, '*_summary.csv')):
            os.remove(file)

        print(f"--- Generating summary tables ---")

        def calc_stats(df, value_col):
            grouped = df.groupby(['language', 'vus'], observed=True)[value_col].agg(
                mean='mean',
                median='median',
                min='min',
                max='max',
                std='std',
                p95=lambda x: np.percentile(x, 95),
                count='count'
            ).reset_index()
            return grouped

        print("Generating summary table [1]")
        df_latency = pd.read_csv(os.path.join(temp_dir, 'latency_filtered.csv'), dtype={
            'language': 'category', 'vus': 'int16', 'latency': 'float32'
        })
        latency_summary = calc_stats(df_latency, 'latency')
        latency_summary.rename(columns={'mean': 'Średni czas odpowiedzi [ms]',
                                        'median': 'Mediana [ms]',
                                        'min': 'Min [ms]',
                                        'max': 'Max [ms]',
                                        'std': 'Odchylenie std [ms]',
                                        'p95': '95-percentyl [ms]',
                                        'count': 'Liczba próbek'}, inplace=True)
        latency_summary.loc[:, latency_summary.columns.difference(['language', 'vus', 'Liczba próbek'])] = \
            latency_summary.loc[:, latency_summary.columns.difference(['language', 'vus', 'Liczba próbek'])].round(3)
        latency_summary.to_csv(os.path.join(output_dir, 'latency_summary.csv'), index=False)
        del df_latency
        gc.collect()

        print("Generating summary table [2]")
        df_rps = pd.read_csv(os.path.join(temp_dir, 'rps_filtered.csv'), dtype={
            'language': 'category', 'vus': 'int16', 'rps': 'float64'
        })
        rps_summary = calc_stats(df_rps, 'rps')
        rps_summary.rename(columns={'mean': 'Średnia RPS',
                                    'median': 'Mediana RPS',
                                    'min': 'Min RPS',
                                    'max': 'Max RPS',
                                    'std': 'Odchylenie std RPS',
                                    'count': 'Liczba pomiarów'}, inplace=True)
        rps_summary.loc[:, rps_summary.columns.difference(['language', 'vus', 'Liczba pomiarów'])] = \
            rps_summary.loc[:, rps_summary.columns.difference(['language', 'vus', 'Liczba pomiarów'])].round(3)
        rps_summary.to_csv(os.path.join(output_dir, 'rps_summary.csv'), index=False)
        del df_rps
        gc.collect()

        print("Generating summary table [3]")
        df_cpu = pd.read_csv(os.path.join(temp_dir, 'cpu_perc_filtered.csv'), dtype={
            'language': 'category', 'vus': 'int16', 'cpu': 'float32'
        })
        cpu_summary = calc_stats(df_cpu, 'cpu')
        cpu_summary.rename(columns={'mean': 'Średnie zużycie CPU [%]',
                                    'median': 'Mediana CPU [%]',
                                    'min': 'Min CPU [%]',
                                    'max': 'Max CPU [%]',
                                    'std': 'Odchylenie std CPU [%]',
                                    'count': 'Liczba próbek'}, inplace=True)
        cpu_summary.loc[:, cpu_summary.columns.difference(['language', 'vus', 'Liczba próbek'])] = \
            cpu_summary.loc[:, cpu_summary.columns.difference(['language', 'vus', 'Liczba próbek'])].round(3)
        cpu_summary.to_csv(os.path.join(output_dir, 'cpu_summary.csv'), index=False)
        del df_cpu
        gc.collect()

        print("Generating summary table [4]")
        df_mem = pd.read_csv(os.path.join(temp_dir, 'mem_mb_filtered.csv'), dtype={
            'language': 'category', 'vus': 'int16', 'mem': 'float32'
        })
        mem_summary = calc_stats(df_mem, 'mem')
        mem_summary.rename(columns={'mean': 'Średnie zużycie RAM [MB]',
                                    'median': 'Mediana RAM [MB]',
                                    'min': 'Min RAM [MB]',
                                    'max': 'Max RAM [MB]',
                                    'std': 'Odchylenie std RAM [MB]',
                                    'count': 'Liczba próbek'}, inplace=True)
        mem_summary.loc[:, mem_summary.columns.difference(['language', 'vus', 'Liczba próbek'])] = \
            mem_summary.loc[:, mem_summary.columns.difference(['language', 'vus', 'Liczba próbek'])].round(3)
        mem_summary.to_csv(os.path.join(output_dir, 'mem_summary.csv'), index=False)
        del df_mem
        gc.collect()

        print("Generating summary table [5]")
        df_fails = pd.read_csv(os.path.join(temp_dir, 'fails.csv'), dtype={
            'language': 'category', 'vus': 'int16', 'fails': 'float32'
        })
        fails_summary = df_fails.groupby(['language', 'vus'], observed=True)['fails'].mean().reset_index()
        fails_summary.rename(columns={'fails': 'Średnia liczba błędów'}, inplace=True)
        fails_summary['Średnia liczba błędów'] = fails_summary['Średnia liczba błędów'].round(3)
        fails_summary.to_csv(os.path.join(output_dir, 'fails_summary.csv'), index=False)
        del df_fails
        gc.collect()

    def generate_plots():
        for file in glob.glob(os.path.join(output_dir, '*.png')):
            os.remove(file)

        print(f"--- Generating plots ---")
        print("Generating plots [1]")
        df_latency_raw = pd.read_csv(os.path.join(temp_dir, 'latency_filtered.csv'), dtype={
            'language': 'category', 'vus': 'int16', 'latency': 'float32'
        })
        for lang_key, lang_pl in languages.items():
            df_lang = df_latency_raw[df_latency_raw['language'] == lang_key]
            plt.figure(figsize=(12,7))
            ax = sns.boxplot(data=df_lang, x='vus', y='latency')
            plt.title(f'Rozkład czasów odpowiedzi dla języka {lang_pl} - Endpoint {endpoint}')
            plt.xlabel('Liczba użytkowników (VUs)')
            plt.ylabel('Czas odpowiedzi [ms]')
            plt.grid(True, linestyle='--', alpha=0.6)
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, f'latency_boxplot_{lang_key}_{endpoint}.png'))
            plt.close()
        del df_latency_raw
        gc.collect()

        df_latency_filtered = pd.read_csv(os.path.join(temp_dir, 'latency_filtered.csv'), dtype={
            'language': 'category', 'vus': 'int16', 'latency': 'float32'
        })
        latency_avg = df_latency_filtered.groupby(['language', 'vus'], observed=True)['latency'].mean().reset_index()
        save_lineplot(latency_avg, 'vus', 'latency', 'language',
                      f'Średni czas odpowiedzi vs liczba użytkowników - Endpoint {endpoint_label}',
                      'Średni czas odpowiedzi [ms]', os.path.join(output_dir, f'latency_avg_lineplot_{endpoint}.png'))
        save_lineplot_with_minmax(df_latency_filtered, 'vus', 'latency', 'language',
                                  f'Czas odpowiedzi – średnia i zakres min–max vs liczba użytkowników - Endpoint {endpoint_label}',
                                  'Czas odpowiedzi [ms]', os.path.join(output_dir, f'latency_avg_minmax_lineplot_{endpoint}.png'))
        del df_latency_filtered
        gc.collect()

        print("Generating plots [2]")
        df_rps = pd.read_csv(os.path.join(temp_dir, 'rps_filtered.csv'), dtype={
            'language': 'category', 'vus': 'int16', 'rps': 'float64'
        })
        for lang_key, lang_pl in languages.items():
            df_rps_lang = df_rps[df_rps['language'] == lang_key]
            plt.figure(figsize=(10,6))
            ax = sns.boxplot(data=df_rps_lang, x='vus', y='rps')
            plt.title(f'Rozkład przepustowości (RPS) dla języka {lang_pl} - Endpoint {endpoint_label}')
            plt.xlabel('Liczba użytkowników (VUs)')
            plt.ylabel('Liczba zapytań na sekundę (RPS)')
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, f'rps_boxplot_{lang_key}_{endpoint}.png'))
            plt.close()

        rps_avg = df_rps.groupby(['language', 'vus'], observed=True)['rps'].mean().reset_index()
        save_lineplot(rps_avg, 'vus', 'rps', 'language',
                      f'Średnia przepustowość (RPS) vs liczba użytkowników - Endpoint {endpoint_label}',
                      'Średnia liczba zapytań na sekundę (RPS)', os.path.join(output_dir, f'rps_avg_lineplot_{endpoint}.png'))
        save_lineplot_with_minmax(df_rps, 'vus', 'rps', 'language',
                                  f'Przepustowość (RPS): średnia z zakresem min–max vs liczba użytkowników - Endpoint {endpoint_label}',
            'Liczba zapytań na sekundę (RPS)', os.path.join(output_dir, f'rps_avg_minmax_lineplot_{endpoint}.png')
        )
        del df_rps
        gc.collect()

        print("Generating plots [3]")
        df_cpu_raw = pd.read_csv(os.path.join(temp_dir, 'cpu_perc_filtered.csv'), dtype={
            'language': 'category', 'vus': 'int16', 'cpu': 'float32'
        })
        for lang_key, lang_pl in languages.items():
            df_cpu_lang = df_cpu_raw[df_cpu_raw['language'] == lang_key]
            plt.figure(figsize=(10,6))
            ax = sns.boxplot(data=df_cpu_lang, x='vus', y='cpu')
            plt.title(f'Rozkład zużycia CPU dla języka {lang_pl} - Endpoint {endpoint_label}')
            plt.xlabel('Liczba użytkowników (VUs)')
            plt.ylabel('Zużycie CPU [%]')
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, f'cpu_boxplot_{lang_key}_{endpoint}.png'))
            plt.close()
        del df_cpu_raw
        gc.collect()

        df_cpu_filtered = pd.read_csv(os.path.join(temp_dir, 'cpu_perc_filtered.csv'), dtype={
            'language': 'category', 'vus': 'int16', 'cpu': 'float32'
        })
        cpu_avg = df_cpu_filtered.groupby(['language', 'vus'], observed=True)['cpu'].mean().reset_index()
        save_lineplot(cpu_avg, 'vus', 'cpu', 'language',
                      f'Średnie zużycie CPU vs liczba użytkowników - Endpoint {endpoint_label}',
                      'Średnie zużycie CPU [%]', os.path.join(output_dir, f'cpu_avg_lineplot_{endpoint}.png'))
        save_lineplot_with_minmax(df_cpu_filtered, 'vus', 'cpu', 'language',
                                  f'Zużycie CPU – średnia i zakres min–max vs liczba użytkowników - Endpoint {endpoint_label}',
                                  'Zużycie CPU [%]', os.path.join(output_dir, f'cpu_avg_minmax_lineplot_{endpoint}.png'))
        del df_cpu_filtered
        gc.collect()

        print("Generating plots [4]")
        df_mem_raw = pd.read_csv(os.path.join(temp_dir, 'mem_perc_filtered.csv'), dtype={
            'language': 'category', 'vus': 'int16', 'mem': 'float32'
        })
        for lang_key, lang_pl in languages.items():
            df_mem_lang = df_mem_raw[df_mem_raw['language'] == lang_key]
            plt.figure(figsize=(10,6))
            ax = sns.boxplot(data=df_mem_lang, x='vus', y='mem')
            plt.title(f'Rozkład zużycia pamięci RAM dla języka {lang_pl} - Endpoint {endpoint_label}')
            plt.xlabel('Liczba użytkowników (VUs)')
            plt.ylabel('Zużycie pamięci RAM [%]')
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, f'mem_boxplot_{lang_key}_{endpoint}.png'))
            plt.close()
        del df_mem_raw
        gc.collect()

        df_mem_filtered = pd.read_csv(os.path.join(temp_dir, 'mem_mb_filtered.csv'), dtype={
            'language': 'category', 'vus': 'int16', 'mem': 'float32'
        })
        mem_avg = df_mem_filtered.groupby(['language', 'vus'], observed=True)['mem'].mean().reset_index()
        save_lineplot(mem_avg, 'vus', 'mem', 'language',
                      f'Średnie zużycie pamięci RAM vs liczba użytkowników - Endpoint {endpoint_label}',
                      'Średnie zużycie pamięci RAM [MB]', os.path.join(output_dir, f'mem_avg_lineplot_{endpoint}.png'))
        save_lineplot_with_minmax(df_mem_filtered, 'vus', 'mem', 'language',
                                  f'Zużycie pamięci RAM – średnia i zakres min–max vs liczba użytkowników - Endpoint {endpoint_label}',
                                  'Zużycie pamięci RAM [MB]', os.path.join(output_dir, f'mem_avg_minmax_lineplot_{endpoint}.png'))
        del df_mem_filtered
        gc.collect()

        print("Generating plots [5]")
        df_fails = pd.read_csv(os.path.join(temp_dir, 'fails.csv'), dtype={
            'language': 'category', 'vus': 'int16', 'fails': 'float32'
        })
        # for lang_key, lang_pl in languages.items():
        #     df_fails_lang = df_fails[df_fails['language'] == lang_key]
        #     fails_avg = df_fails_lang.groupby('vus')['fails'].mean().reset_index()
        #     plt.figure(figsize=(10,6))
        #     ax = sns.barplot(data=fails_avg, x='vus', y='fails')
        #     plt.title(f'Średnia liczba błędnych odpowiedzi vs liczba użytkowników - {lang_pl} - Endpoint {endpoint_label}')
        #     plt.xlabel('Liczba użytkowników (VUs)')
        #     plt.ylabel('Średnia liczba błędów')
        #     plt.grid(True, linestyle='--', alpha=0.7)
        #     plt.tight_layout()
        #     plt.savefig(os.path.join(output_dir, f'fails_barplot_{lang_key}_{endpoint}.png'))
        #     plt.close()

        fails_avg_all = df_fails.groupby(['language', 'vus'], observed=True)['fails'].mean().reset_index()
        plt.figure(figsize=(12,7))
        ax = sns.barplot(data=fails_avg_all, x='vus', y='fails', hue='language')
        handles, labels = ax.get_legend_handles_labels()
        labels_pl = [languages.get(label, label) for label in labels]
        ax.legend(handles, labels_pl, title='Język')
        plt.title(f'Średnia liczba błędnych odpowiedzi vs liczba użytkowników – wszystkie języki – Endpoint {endpoint_label}')
        plt.xlabel('Liczba użytkowników (VUs)')
        plt.ylabel('Średnia liczba błędów')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'fails_barplot_all_{endpoint}.png'))
        plt.close()
        del df_fails
        gc.collect()

        print("Generating plots [6]")
        df_waiting = pd.read_csv(os.path.join(temp_dir, 'waiting_filtered.csv'), dtype={
            'language': 'category', 'vus': 'int16', 'waiting': 'float32'
        })
        waiting_avg = df_waiting.groupby(['language', 'vus'], observed=True)['waiting'].mean().reset_index()
        save_lineplot(waiting_avg, 'vus', 'waiting', 'language',
                      f'Średni czas przetwarzania backendu vs liczba użytkowników - Endpoint {endpoint_label}',
                      'Czas oczekiwania na odpowiedź [ms]',
                      os.path.join(output_dir, f'waiting_avg_lineplot_{endpoint}.png'))
        del df_waiting
        gc.collect()

        print("Generating plots [7]")
        df_mem_perc = pd.read_csv(os.path.join(temp_dir, 'mem_perc_filtered.csv'), dtype={
            'language': 'category', 'vus': 'int16', 'mem': 'float32'
        })
        mem_perc_avg = df_mem_perc.groupby(['language', 'vus'], observed=True)['mem'].mean().reset_index()
        save_lineplot(mem_perc_avg, 'vus', 'mem', 'language',
                      f'Procentowe zużycie pamięci RAM względem limitu 4 GB vs liczba użytkowników - Endpoint {endpoint_label}',
                      'Zużycie pamięci [%]',
                      os.path.join(output_dir, f'mem_percent_lineplot_{endpoint}.png'))
        del df_mem_perc
        gc.collect()

    if new_analyse:
        process_new_analyse()
    if new_summary:
        generate_summary_tables()
    if new_plots:
        generate_plots()
    print(f"Done in {(time.time() - s_time):.2f}s")

if __name__ == '__main__':
    s_start = time.time()

    #main("ping", "/ping", False)
    #main("fibonacci", "/math/fibonacci", False)
    #main("error", "/error", False, True, True)
    main("fibonacci_iter", "/math/fibonacci-iter", False, True, True)
    #main("fibonacci_error", "/math/fibonacci/error")
    #main("matrix_int", "/math/matrix/int")
    #main("matrix_float", "/math/matrix/float")
    #main("upload_json","upload_json")

    print(f"Done all in {(time.time() - s_start):.2f}s")
