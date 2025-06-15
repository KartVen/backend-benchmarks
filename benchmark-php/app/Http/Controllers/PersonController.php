<?php

namespace App\Http\Controllers;

use App\Models\Person;
use Illuminate\Http\Request;

class PersonController extends Controller
{
    public function store(Request $request)
    {
        $person = Person::create($request->only(['name', 'email']));
        return response()->json($person);
    }

    public function index()
    {
        return response()->json(Person::all());
    }

    public function show($id)
    {
        $person = Person::find($id);
        return $person ? response()->json($person) : response('', 404);
    }

    public function update(Request $request, $id)
    {
        $person = Person::find($id);
        if (!$person) return response('', 404);
        $person->update($request->only(['name', 'email']));
        return response()->json($person);
    }

    public function destroy($id)
    {
        $person = Person::find($id);
        if (!$person) return response('', 404);
        $person->delete();
        return response('', 200);
    }
}
