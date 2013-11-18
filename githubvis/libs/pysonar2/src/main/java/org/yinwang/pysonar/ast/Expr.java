package org.yinwang.pysonar.ast;

import org.jetbrains.annotations.NotNull;
import org.yinwang.pysonar.Indexer;
import org.yinwang.pysonar.Scope;
import org.yinwang.pysonar.types.Type;

/**
 * Expression statement.
 */
public class Expr extends Node {

    static final long serialVersionUID = 7366113211576923188L;

    public Node value;


    public Expr(Node n, int start, int end) {
        super(start, end);
        this.value = n;
        addChildren(n);
    }

    @Override
    public Type resolve(Scope s, int tag) {
        if (value != null) resolveExpr(value, s, tag);
        return Indexer.idx.builtins.Cont;
    }

    @NotNull
    @Override
    public String toString() {
        return "<ExprStmt:" + value + ">";
    }

    @Override
    public void visit(@NotNull NodeVisitor v) {
        if (v.visit(this)) {
            visitNode(value, v);
        }
    }
}
