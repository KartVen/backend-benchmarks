<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class MathController extends Controller
{
    public function fibonacci(Request $request)
    {
        $n = (int)$request->query('n', 30);
        return response((string)$this->fib($n), 200)->header("Content-Type", "text/plain");
    }

    public function fibonacciIter(Request $request)
    {
        $n = (int)$request->query('n', 30);
        if ($n <= 1) return response((string)$n, 200)->header("Content-Type", "text/plain");

        $a = 0;
        $b = 1;
        for ($i = 2; $i <= $n; $i++) {
            $temp = $a + $b;
            $a = $b;
            $b = $temp;
        }

        return response((string)$b, 200)->header("Content-Type", "text/plain");
    }

    public function fibonacciError(Request $request)
    {
        $n = (int)$request->query('n', 30);
        return response((string)$this->fibWithError($n), 200)->header("Content-Type", "text/plain");
    }

    private function fib($n)
    {
        if ($n <= 1) return $n;
        return $this->fib($n - 1) + $this->fib($n - 2);
    }

    private function fibWithError($n)
    {
        if ($n === 1) {
            abort(500, 'Error while processing');
        }
        if ($n <= 0) return 0;
        return $this->fibWithError($n - 1) + $this->fibWithError($n - 2);
    }

    public function multiplyInt(Request $request)
    {
        $A = $request->input('a');
        $B = $request->input('b');
        $n = count($A);
        $m = count($A[0]);
        $k = count($B[0]);
        $result = [];

        for ($i = 0; $i < $n; $i++) {
            $result[$i] = [];
            for ($j = 0; $j < $k; $j++) {
                $sum = 0;
                for ($l = 0; $l < $m; $l++) {
                    $sum += $A[$i][$l] * $B[$l][$j];
                }
                $result[$i][$j] = $sum;
            }
        }

        return response()->json($result);
    }

    public function multiplyFloat(Request $request)
    {
        $A = $request->input('a');
        $B = $request->input('b');
        $n = count($A);
        $m = count($A[0]);
        $k = count($B[0]);
        $result = [];

        for ($i = 0; $i < $n; $i++) {
            $result[$i] = [];
            for ($j = 0; $j < $k; $j++) {
                $sum = 0.0;
                for ($l = 0; $l < $m; $l++) {
                    $sum += (float)$A[$i][$l] * (float)$B[$l][$j];
                }
                $result[$i][$j] = $sum;
            }
        }

        return response()->json($result);
    }
}
