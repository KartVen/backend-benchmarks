<?php

namespace App\Exceptions;

use Throwable;
use Illuminate\Foundation\Exceptions\Handler as ExceptionHandler;

class Handler extends ExceptionHandler
{
    protected $levels = [];

    protected $dontReport = [];

    protected $dontFlash = [
        'current_password',
        'password',
        'password_confirmation',
    ];

    public function register(): void
    {
        //
    }

    public function render($request, Throwable $e)
    {
        $status = method_exists($e, 'getStatusCode')
            ? $e->getStatusCode()
            : 500;

        return response()->json([
            'message' => $e->getMessage() ?: 'Unexpected error',
            'exception' => class_basename($e),
            'status' => $status,
            'timestamp' => now()->toISOString(),
            'path' => '/' . ltrim($request->path(), '/'),
        ], $status);
    }
}
