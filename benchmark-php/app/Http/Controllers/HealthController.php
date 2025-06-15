<?php

namespace App\Http\Controllers;

use Illuminate\Http\Response;

class HealthController extends Controller
{
    public function ping()
    {
        return response("OK", 200)->header('Content-Type', 'text/plain');
    }
}
