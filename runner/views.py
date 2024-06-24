from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import subprocess
import os
import tempfile
from courses.models import Assignment, TestCase

@csrf_exempt
def interpreter(request):
    inputs = request.POST.get('inputs', '')
    print(request.POST)
    if request.method == 'POST':
        code = request.POST.get('code', '')
        try:
            result = run_user_code(code,inputs)
            return JsonResponse({'result': result})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def checker(request):
    assignment_id = int(request.POST.get('assignment_id'))
    if request.method == 'POST':
        code = request.POST.get('code', '')
        assignment = get_object_or_404(Assignment, id=assignment_id)
        results = []

        for test_case in assignment.test_cases.all():
            input_values = test_case.input_values.split(',')
            expected_output = test_case.expected_output
            result = run_user_code_with_test(code, input_values, expected_output)
            results.append(result)

        return JsonResponse(results, safe=False)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def run_user_code(user_code, inputs):
    inputs=inputs.split(',')
    with tempfile.NamedTemporaryFile(delete=False, suffix='.py', mode='w') as temp_file:
        temp_file.write(user_code)
        temp_file.flush()
        temp_file_name = temp_file.name
    try:
        process = subprocess.Popen(
            ['python', temp_file_name] + inputs,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate(input='\n'.join(inputs).encode('utf-8'))
        result = stdout.decode('utf-8') + stderr.decode('utf-8')
        
    finally:
        os.remove(temp_file_name) 
    return result

def run_user_code_with_test(user_code, input_values, expected_output):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.py') as temp_file:
        temp_file.write(user_code.encode('utf-8'))
        temp_file.flush()
        temp_file_name = temp_file.name
    try:
        process = subprocess.Popen(
            ['python', temp_file_name] + input_values,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate(input='\n'.join(input_values).encode('utf-8'))
        actual_output = stdout.decode('utf-8')
        if actual_output == expected_output:
            return {'input': input_values, 'output': actual_output, 'result': 'Success'}
        else:
            return {'input': input_values, 'output': actual_output, 'result': 'Failed', 'expected': expected_output}
    except subprocess.TimeoutExpired:
        return {'input': input_values, 'result': 'Error', 'error': 'Execution timed out'}
    except Exception as e:
        return {'input': input_values, 'result': 'Error', 'error': str(e)}
    finally:
        os.remove(temp_file_name)