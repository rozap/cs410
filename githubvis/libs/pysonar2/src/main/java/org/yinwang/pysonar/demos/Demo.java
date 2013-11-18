package org.yinwang.pysonar.demos;

import org.jetbrains.annotations.NotNull;
import org.yinwang.pysonar.Indexer;
import org.yinwang.pysonar.Progress;
import org.yinwang.pysonar.Util;

import java.io.File;
import java.util.List;


public class Demo {

    private static File OUTPUT_DIR;

    private static final String CSS =
            "body { color: #666666; } \n" +
                    "a {text-decoration: none; color: #5A82F7}\n" +
                    "table, th, td { border: 1px solid lightgrey; padding: 5px; corner: rounded; }\n" +
                    ".builtin {color: #B17E41;}\n" +
                    ".comment, .block-comment {color: #aaaaaa; font-style: italic;}\n" +
                    ".constant {color: #888888;}\n" +
                    ".decorator {color: #778899;}\n" +
                    ".doc-string {color: #aaaaaa;}\n" +
                    ".error {border-bottom: 1px solid red;}\n" +
                    ".field-name {color: #2e8b57;}\n" +
                    ".function {color: #4682b4;}\n" +
                    ".identifier {color: #8b7765;}\n" +
                    ".info {border-bottom: 1px dotted RoyalBlue;}\n" +
                    ".keyword {color: #0000cd;}\n" +
                    ".lineno {color: #aaaaaa;}\n" +
                    ".number {color: #483d8b;}\n" +
                    ".parameter {color: #777777;}\n" +
                    ".string {color: #999999;}\n" +
                    ".type-name {color: #4682b4;}\n" +
                    ".warning {border-bottom: 1px dotted orange;}\n";

    private static final String JS =
            "<script language=\"JavaScript\" type=\"text/javascript\">\n" +
                    "var highlighted = new Array();\n" +
                    "function highlight()\n" +
                    "{\n" +
                    "    // clear existing highlights\n" +
                    "    for (var i = 0; i < highlighted.length; i++) {\n" +
                    "        var elm = document.getElementById(highlighted[i]);\n" +
                    "        if (elm != null) {\n" +
                    "            elm.style.backgroundColor = 'white';\n" +
                    "        }\n" +
                    "    }\n" +
                    "    highlighted = new Array();\n" +
                    "    for (var i = 0; i < arguments.length; i++) {\n" +
                    "        var elm = document.getElementById(arguments[i]);\n" +
                    "        if (elm != null) {\n" +
                    "            elm.style.backgroundColor='gold';\n" +
                    "        }\n" +
                    "        highlighted.push(arguments[i]);\n" +
                    "    }\n" +
                    "} </script>\n";


    private Indexer indexer;
    private String rootPath;
    private Linker linker;

    private void makeOutputDir() {
        if (!OUTPUT_DIR.exists()) {
            OUTPUT_DIR.mkdirs();
            Util.msg("Created directory: " + OUTPUT_DIR.getAbsolutePath());
        }
    }

    private void start(@NotNull File fileOrDir) throws Exception {
        long start = System.currentTimeMillis();

        File rootDir = fileOrDir.isFile() ? fileOrDir.getParentFile() : fileOrDir;
        try {
            rootPath = rootDir.getCanonicalPath();
        } catch (Exception e) {
            Util.die("File not found: " + fileOrDir);
        }

        indexer = new Indexer();

        Util.msg("Building index");

        indexer.loadFileRecursive(fileOrDir.getCanonicalPath());

        indexer.finish();

        Util.msg(indexer.getStatusReport());

        long end = System.currentTimeMillis();
        Util.msg("Finished indexing in: " + Util.timeString(end - start));

        start = System.currentTimeMillis();
        generateJSON();
        end = System.currentTimeMillis();
        Util.msg("Finished generating JSON in: " + Util.timeString(end - start));
        indexer.close();
    }


    private void generateJSON() {
        Util.msg("\nGenerating JSON");
        makeOutputDir();

        linker = new Linker(rootPath, OUTPUT_DIR);
        linker.findLinks(indexer);

        int rootLength = rootPath.length();
        Progress progress = new Progress(100, 100);


        File destFile = Util.joinPath(OUTPUT_DIR, "output");
        destFile.getParentFile().mkdirs();
        String destPath = destFile.getAbsolutePath() + ".json";
        String jsonThing = markup(destPath);
        try {
            Util.writeFile(destPath, jsonThing);
        } catch (Exception e) {
            Util.msg("Failed to write: " + destPath);
        }


        progress.end();
        Util.msg("Wrote " + indexer.getLoadedFiles().size() + " files to " + OUTPUT_DIR);
    }

    @NotNull
    private String markup(String path) {
        return new PrettyPrinter(indexer).generate(path);
    }

    @NotNull
    private String addLineNumbers(@NotNull String source) {
        StringBuilder result = new StringBuilder((int) (source.length() * 1.2));
        int count = 1;
        for (String line : source.split("\n")) {
            result.append("<span class='lineno'>");
            result.append(count++);
            result.append("</span> ");
            result.append(line);
            result.append("\n");
        }
        return result.toString();
    }


    private static void usage() {
        Util.msg("Usage:  java -jar pysonar-2.0-SNAPSHOT.jar <file-or-dir> <output-dir>");
        Util.msg("Example that generates an index for Python 2.7 standard library:");
        Util.msg(" java -jar pysonar-2.0-SNAPSHOT.jar /usr/lib/python2.7 ./html");
        System.exit(0);
    }

    @NotNull
    private static File checkFile(String path) {
        File f = new File(path);
        if (!f.canRead()) {
            Util.die("Path not found or not readable: " + path);
        }
        return f;
    }

    public static void main(@NotNull String[] args) throws Exception {
        if (args.length != 2) {
            usage();
        }

        File fileOrDir = checkFile(args[0]);
        OUTPUT_DIR = new File(args[1]);

        new Demo().start(fileOrDir);
    }
}
