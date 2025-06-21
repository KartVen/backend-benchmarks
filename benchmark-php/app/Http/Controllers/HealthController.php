<?php

namespace App\Http\Controllers;

use Symfony\Component\HttpKernel\Exception\HttpException;

class HealthController extends Controller
{
    public function ping()
    {
        return response("OK", 200)->header("Content-Type", "text/plain");
    }

    public function error()
    {
        throw new HttpException(500, 'Simulated exception');
    }
}
