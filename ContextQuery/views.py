from VDBforGenAI.VectorDatabase import VectorDatabase
from django.shortcuts import render
import json
import torch
from django.http import FileResponse
from Query.views import generate_bot_response

f = open('config.json')

config = json.load(f)
if config['embedding_model']:
    hidden_size=config['embedding_model_hidden_size']
    VDB = VectorDatabase(encoder=config['embedding_model'], splitting_choice='length', hidden_size=hidden_size)
    VDB.load_all_in_directory(config['loading_dir'])
else:
    VDB = VectorDatabase(splitting_choice='length')
    VDB.load_all_in_directory(config['loading_dir'])
reversed_indices_to_names = {value: key for key, value in VDB.list_dict_value_num[-1].items()}


def extract_keys_with_multiple_items(input_dict):
    result = {}

    for key, value_list in input_dict.items():
        if isinstance(value_list, dict):
            if len(value_list) > 1:
                result[str(key)] = list(value_list.keys())

    return result


@torch.inference_mode()
def get_chat_completions_with_context(request):
    messages = request.session.get('messages', [{'role': 'bot', 'content': 'Hello! How can I assist you?'}])
    passed_selection = extract_keys_with_multiple_items(VDB.list_dict_value_num)

    if request.method == 'POST':
        # Get the user input from the form
        message = request.POST.get('message')
        messages.append({'role': 'user', 'content': message})
        prepending = "A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions and tries to use the provided context to answer the user's questions. User:"
        i1, i2 = VDB.get_context_indices_from_entire_database(message)
        context_small = VDB.list_of_lists_of_strings[i1][i2]
        Context = 'Context:' + context_small
        messages.append({'role': 'context', 'content': Context})

        appending = "Bot:"
        total = prepending + Context + message + appending
        bot_response = generate_bot_response(total)
        messages.append({'role': 'bot', 'content': bot_response})
        request.session['messages'] = messages

        context = {'messages': messages,
                   'pdf_to_show': str(i1),
                   'txt_to_show': '',
                   'highlight_text': context_small,
                   'port': ' 127.0.0.1' + str(config['default_port']),
                   'dictionary_levels_values': passed_selection}
    else:
        context = {'messages': messages,
                   'pdf_to_show': '',
                   'txt_to_show': '',
                   'highlight_text': None,
                   'port': None,
                   'dictionary_levels_values': passed_selection
                   }
    # Render the template with the messages
    return render(request, 'Context.html', context)


def get_names(i1):
    return VDB.list_locations[i1]


def view_pdf(request, file_path):
    # open the file in binary mode
    with open(file_path, 'rb') as pdf:
        response = FileResponse(pdf, content_type='application/pdf')
        # optionally, you can set a filename to display in the user's browser
        response['Content-Disposition'] = 'inline; filename="document.pdf"'
        return response
