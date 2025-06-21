import http from 'k6/http';
import { check } from 'k6';

export const options = {
    scenarios: {
        ramping_vus: {
            executor: 'ramping-vus',
            stages: [
                {duration: '1s', target: __ENV.VUS},
                {duration: __ENV.DURATION, target: __ENV.VUS},
                {duration: '0s', target: 0},
            ],
            gracefulRampDown: '0s',
            gracefulStop: '30s'
        }
    },
};

export default function () {
    const n = 30;
    const res = http.get(`http://localhost:${__ENV.PORT}/math/fibonacci-iter?n=${n}`);
    check(res, {
        'status is 200': (r) => r?.status === 200,
        'correct result': (r) => r?.status === 200 && r?.body?.trim() === '832040',
    });
}
