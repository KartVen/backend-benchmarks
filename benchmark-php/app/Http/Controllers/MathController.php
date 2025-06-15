<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class MathController extends Controller
{
    public function fibonacci(Request $request)
    {
        $n = (int) $request->query('n', 30);
        return response((string) $this->fib($n), 200)
            ->header("Content-Type", "text/plain");
    }

    private function fib($n)
    {
        if ($n <= 1) return $n;
        return $this->fib($n - 1) + $this->fib($n - 2);
    }
}
