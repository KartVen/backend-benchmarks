<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\HealthController;
use App\Http\Controllers\MathController;
use App\Http\Controllers\PersonController;

Route::get('/ping', [HealthController::class, 'ping']);
Route::get('/error', [HealthController::class, 'error']);

Route::get('/math/fibonacci', [MathController::class, 'fibonacci']);
Route::get('/math/fibonacci-iter', [MathController::class, 'fibonacciIter']);
Route::get('/math/fibonacci/error', [MathController::class, 'fibonacciError']);
Route::post('/math/matrix/int', [MathController::class, 'multiplyInt']);
Route::post('/math/matrix/float', [MathController::class, 'multiplyFloat']);

Route::post('/upload-json', [PersonController::class, 'uploadJson']);
