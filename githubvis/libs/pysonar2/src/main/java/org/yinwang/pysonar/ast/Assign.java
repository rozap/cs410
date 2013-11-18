package org.yinwang.pysonar.ast;

import org.jetbrains.annotations.NotNull;
import org.yinwang.pysonar.Indexer;
import org.yinwang.pysonar.Scope;
import org.yinwang.pysonar.types.Type;

import java.util.List;

public class Assign extends Node {

    static final long serialVersionUID = 928890389856851537L;

    public List<Node> targets;
    public Node rvalue;

    public Assign(List<Node> targets, Node rvalue, int start, int end) {
        super(start, end);
        this.targets = targets;
        this.rvalue = rvalue;
        addChildren(targets);
        addChildren(rvalue);
    }

    @Override
    public boolean bindsName() {
        return true;
    }

    @Override
    public Type resolve(@NotNull Scope s, int tag) {
        if (rvalue == null) {
            Indexer.idx.putProblem(this, "missing RHS of assignment");
        } else {
            Type valueType = resolveExpr(rvalue, s, tag);
            for (Node t : targets) {
                NameBinder.bind(s, t, valueType, tag);
            }
        }

        return Indexer.idx.builtins.Cont;
    }

    @NotNull
    @Override
    public String toString() {
        return "<Assign:" + targets + "=" + rvalue + ">";
    }

    @Override
    public void visit(@NotNull NodeVisitor v) {
        if (v.visit(this)) {
            visitNodeList(targets, v);
            visitNode(rvalue, v);
        }
    }
}
