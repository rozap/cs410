package org.yinwang.pysonar.demos;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import org.jetbrains.annotations.NotNull;

import org.yinwang.pysonar.Indexer;
import org.yinwang.pysonar.Outliner;

import org.yinwang.pysonar.ast.FunctionDef;

import java.util.*;


class PrettyPrinter {

    private Indexer indexer;

    public PrettyPrinter(Indexer idx) {
        this.indexer = idx;
    }


    @NotNull
    public String generate(String path) {
        List<Outliner.Entry> entries = generateOutline(indexer, path);

        HashMap<String, ArrayList<String>> callsAsString = new HashMap<>();
        HashMap<FunctionDef, ArrayList<FunctionDef>> funcCalls =  indexer.getFunctionCalls();
        Iterator it = funcCalls.entrySet().iterator();
        while(it.hasNext()) {
            Map.Entry<FunctionDef, ArrayList<FunctionDef>> pair = (Map.Entry<FunctionDef, ArrayList<FunctionDef>>)it.next();
            FunctionDef caller = pair.getKey();
            ArrayList<FunctionDef> calls = pair.getValue();

            //Put them in the new map
            ArrayList<String> callees = new ArrayList<>();
            for(FunctionDef fdef : calls) {
                callees.add(fdef.toString());
            }

            callsAsString.put(caller.toString(), callees);


        }

        Gson gson = new GsonBuilder().setPrettyPrinting().create();
        return gson.toJson(callsAsString).toString();
    }


    @NotNull
    public List<Outliner.Entry> generateOutline(Indexer indexer, @NotNull String file) {
        return new Outliner().generate(indexer, file);
    }

}
