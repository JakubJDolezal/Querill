import json
import os

import requests
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from transformers import LlamaForCausalLM, LlamaTokenizer, AutoConfig, AutoModelForCausalLM
from accelerate import dispatch_model, load_checkpoint_and_dispatch, init_empty_weights
import json
from Query.compression import compress_module
import torch
from django.http import JsonResponse
f = open('config.json')

config = json.load(f)
if config['local_model']:
    if not config['load_8bit']:
        os.environ['CUDA_VISIBLE_DEVICES'] = config['CUDA_VISIBLE_DEVICES']
        config_model = AutoConfig.from_pretrained(config['model_directory'] + '\\config.json')
        with init_empty_weights():
            model = AutoModelForCausalLM.from_config(config_model)
        model.tie_weights()

        model = load_checkpoint_and_dispatch(
            model, config['model_directory'], device_map="auto", no_split_module_classes=["LlamaDecoderLayer"]
        )
    else:
        device = config['device']
        model = AutoModelForCausalLM.from_pretrained(
            config['model_directory'], low_cpu_mem_usage=True,
        )
        compress_module(model, device)
        model = model.to(device)
    tokenizer = LlamaTokenizer.from_pretrained(config['model_directory'])


@torch.inference_mode()
def get_chat_completions(request):
    messages = request.session.get('messages', [ {'role': 'bot', 'content': 'Hello! How can I assist you?'}])
    if request.method == 'POST':
        # Get the user input from the form
        message = request.POST.get('message')
        messages.append({'role': 'user', 'content': message})
        prepending = "A chat between a curious user and an artificial intelligence assistant.The assistant gives helpful, detailed, and polite answers to the user's questions. User:"
        appending = "Bot:"
        total = prepending + message + appending
        bot_response = generate_bot_response(total)
        messages.append({'role': 'bot', 'content': bot_response})
        request.session['messages'] = messages


    # Render the template with the messages
    return render(request, 'Index.html', {'messages': messages})

@csrf_exempt
def api(request):
    if request.method == 'POST':
        # Get the user's message from the request data
        message = request.POST['message']

        # Call a function to generate the bot's response
        prepending = "A chat between a curious user and an artificial intelligence assistant.The assistant gives helpful, detailed, and polite answers to the user's questions. User:"
        appending = "Bot:"
        total = prepending + message + appending
        bot_response = generate_bot_response(total)
        # Construct the response data with the bot's message
        response_data = {
            'response': bot_response
        }

        return JsonResponse(response_data)

    # Return an error response if the request method is not POST
    return JsonResponse({'error': 'Invalid request method'})

def generate_bot_response(message):
    if config['local_model']:
        inputs = tokenizer.encode_plus(message, return_tensors='pt')
        len_input = inputs['input_ids'].size(dim=1)
        outputs = model.generate(inputs['input_ids'].to(device), max_length=int(config["max_response"])).cpu()
        response = tokenizer.decode(outputs[0][len_input:], skip_special_tokens=True)
    # response = 'Random Response'
        return response

# # Construct the JSON data
# data = {
#     'model': 'vicuna-7b-v1.1',
#     'messages': messages
# }
#
# # Call the API endpoint
# response = requests.post(
#     'http://localhost:8000/v1/chat/completions',
#     json=data,
#     headers={'Content-Type': 'application/json'}
# )

# # Get the completions from the API response
# completions = response.json()['completions']
#
# # Append the bot response to the messages list