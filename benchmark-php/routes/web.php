<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\HealthController;
use App\Http\Controllers\MathController;
use App\Http\Controllers\PersonController;

Route::get('/ping', [HealthController::class, 'ping']);
Route::get('/math/fibonacci', [MathController::class, 'fibonacci']);

Route::prefix('persons')->group(function () {
    Route::post('/', [PersonController::class, 'store']);
    Route::get('/', [PersonController::class, 'index']);
    Route::get('/{id}', [PersonController::class, 'show']);
    Route::put('/{id}', [PersonController::class, 'update']);
    Route::delete('/{id}', [PersonController::class, 'destroy']);
});
