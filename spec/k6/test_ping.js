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
    const res = http.get(`http://localhost:${__ENV.PORT}/ping`);
    check(res, {
        'status is 200': (r) => r.status === 200,
        'body is OK': (r) => r.body === 'OK',
    });
}
