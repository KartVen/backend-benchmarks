<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class PersonController extends Controller
{
    public function uploadJson(Request $request)
    {
        $gmailCount = collect($request->json()->all())->filter(fn($p) => isset($p['email']) && str_contains($p['email'], 'gmail.com'))->count();
        return response()->json(['gmailCount' => $gmailCount]);
    }
}
