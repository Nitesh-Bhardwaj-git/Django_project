from django.views import View
from django.shortcuts import render
import ast
import operator

class CalculatorView(View):
    def get(self, request):
        return render(request, 'Calculator_app/calculator.html')

    def post(self, request):
        result = None
        error = None
        expr = request.POST.get('expression', '')
        if expr:
            try:
                # Safe evaluation using ast
                result = self.safe_eval(expr)
            except Exception:
                error = 'Invalid expression.'
        else:
            error = 'No input.'
        context = {'result': result}
        if error:
            context['error'] = error
        return render(request, 'Calculator_app/calculator.html', context)

    def safe_eval(self, expr):
        
        allowed_operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.USub: operator.neg
        }
        def eval_node(node):
            if isinstance(node, ast.Constant):
                return node.n
            elif isinstance(node, ast.BinOp):
                left = eval_node(node.left)
                right = eval_node(node.right)
                op_type = type(node.op)
                if op_type in allowed_operators:
                    return allowed_operators[op_type](left, right)
                else:
                    raise ValueError('Operator not allowed')
            elif isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
                return -eval_node(node.operand)
            else:
                raise ValueError('Invalid expression')
        node = ast.parse(expr, mode='eval').body
        return eval_node(node)
