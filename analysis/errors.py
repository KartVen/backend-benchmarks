import glob
import pandas as pd
import os

languages = ['java', 'csharp', 'python', 'php']
endpoint = 'ping'
metrics_base_dir = '/media/kartven/Backup Drive/spec/metrics'

for lang in languages:
    metrics_dir = os.path.join(metrics_base_dir, lang)
    metrics_path = os.path.join(metrics_dir, f'{endpoint}_10_30_step_*.csv')
    files = sorted(glob.glob(metrics_path))

    errors_info = []

    print(f"Checking errors for language '{lang}':")
    for idx, f in enumerate(files, start=1):
        print(f"  [{lang}] Loading metric file {idx}/{len(files)}: {os.path.basename(f)}")
        df = pd.read_csv(f)
        failed_df = df[df['metric_name'] == 'http_req_failed']
        if not failed_df.empty:
            total_failed = failed_df['metric_value'].sum()
            if total_failed > 0:
                step = os.path.basename(f).split('_step_')[1].replace('.csv', '')
                errors_info.append((step, total_failed))

    if errors_info:
        for step, count in errors_info:
            print(f"  Step {step}: {count} failed requests")
    else:
        print("  No failed requests detected.")
    print()
