import requests
from translations_list import translations
from key_vault import token


bearer_token = token

endpoint_url = "https://composer.opera-api.com/api/v1/prompts/translate"
headers = {
    'Authorization': f'Bearer {bearer_token}',
    'accept': 'application/json',
    'x-opera-timezone': 'Z',
    'Content-Type': 'application/json',
    'X-Opera-UI-Language': 'pl'
}
payload = {
    'selected_text': 'Test Translation AI provided by Opera'
}


# Test for Successful Translation
def test_successful_translation():
    assertion_results = []
    for translation in translations:
        headers_translate = headers.copy()
        headers_translate['X-Opera-UI-Language'] = translation[0]
        payload_translate = {'selected_text': translation[2]}
        response_translate = requests.post(endpoint_url, headers=headers_translate, json=payload_translate)
        assert response_translate.status_code == 200, 'Invalid response code'
        assert 'message' in response_translate.json()
        assert 'finish_reason' in response_translate.json()
        assert 'requests_available' in response_translate.json()
        assert 'requests_max' in response_translate.json()
        assert 'conversation_id' in response_translate.json()
        assert 'title' in response_translate.json()
        try:
            assert translation[1] == response_translate.json().get(
                'message'), f"Expected translation: '{translation[1]}', Actual translation: '{response_translate.json().get('message')}'"
            assertion_results.append(True)
        except AssertionError as ae:
            print('Invalid translation:')
            print(f"Expected translation: '{translation[1]}'")
            print(f"Actual translation: '{response_translate.json().get('message')}'")
            assertion_results.append(False)
    if all(assertion_results):
        print("All translations passed successfully!")
    else:
        print("Some translations failed!")
        assert False


# Test for Conversation Continuation
def test_conversation_continuation_en():
    headers_continuation = headers.copy()
    headers_continuation['X-Opera-UI-Language'] = 'en'
    payload_initial = {'selected_text': 'Text translation API check'}
    response_initial = requests.post(endpoint_url, headers=headers_continuation, json=payload_initial)
    assert response_initial.status_code == 200, 'Invalid response code'
    assert 'message' in response_initial.json()
    assert 'finish_reason' in response_initial.json()
    assert 'requests_available' in response_initial.json()
    assert 'requests_max' in response_initial.json()
    assert 'conversation_id' in response_initial.json()
    assert 'title' in response_initial.json()
    conversation_id = response_initial.json().get('conversation_id')

    # Continue conversation with conversation_id
    payload_continuation = {'selected_text': 'continue conversation', 'conversation_id': conversation_id}
    response_continuation = requests.post(endpoint_url, headers=headers_continuation, json=payload_continuation)
    assert response_continuation.status_code == 200, 'Invalid response code'
    assert 'message' in response_continuation.json()
    assert 'finish_reason' in response_continuation.json()
    assert 'requests_available' in response_continuation.json()
    assert 'requests_max' in response_continuation.json()
    assert 'conversation_id' in response_continuation.json()
    assert 'title' in response_continuation.json()
    assert "Sure, let's continue the conversation. What would you like to talk about?" == response_continuation.json().get('message')


# Test for Missing Authorization
def test_missing_authorization():
    headers_without_auth = headers.copy()
    del headers_without_auth['Authorization']
    response = requests.post(endpoint_url, headers=headers_without_auth, json=payload)
    assert response.status_code == 401, 'Invalid response code'


# Test for Invalid Language
def test_invalid_language():
    headers_invalid_lang = headers.copy()
    headers_invalid_lang['X-Opera-UI-Language'] = 'invalid_language'
    response = requests.post(endpoint_url, headers=headers_invalid_lang, json=payload)
    assert response.status_code in [400, 422], 'Invalid response code'


# Test for empty Language
def test_empty_language():
    headers_empty_lang = headers.copy()
    headers_empty_lang['X-Opera-UI-Language'] = ''
    response = requests.post(endpoint_url, headers=headers_empty_lang, json=payload)
    assert response.status_code in [400, 422], 'Invalid response code'


# Test for missing Language in header
def test_missing_language():
    headers_missing_lang = headers.copy()
    del headers_missing_lang['X-Opera-UI-Language']
    response = requests.post(endpoint_url, headers=headers_missing_lang, json=payload)
    assert response.status_code in [400, 422], 'Invalid response code'


# Test for invalid json Text
def test_invalid_body():
    response = requests.post(endpoint_url, headers=headers, json={"text": "Text to translate"})
    assert response.status_code == 422, 'Invalid response code'


# Test for empty selected_text in Body
def test_empty_text_body():
    response = requests.post(endpoint_url, headers=headers, json={'selected_text': ''})
    assert response.status_code == 422, 'Invalid response code'


# Test for empty body in endpoint
def test_empty_body():
    response = requests.post(endpoint_url, headers=headers, json={})
    assert response.status_code == 422, 'Invalid response code'


# Test for invalid body parameter in Body
def test_invalid_body_parameter():
    response = requests.post(endpoint_url, headers=headers, json={"selected_text": "Text to translate", "Invalid": "0000"})
    assert response.status_code == 422, 'Invalid response code'


# Test for empty x-opera-timezone in Header
def test_empty_timezone():
    headers_invalid_timezone = headers.copy()
    headers_invalid_timezone['x-opera-timezone'] = ''
    response = requests.post(endpoint_url, headers=headers_invalid_timezone, json=payload)
    assert response.status_code == 422, 'Invalid response code'


# Test for missing x-opera-timezone in Header
def test_missing_timezone():
    headers_missing_timezone = headers.copy()
    del headers_missing_timezone['x-opera-timezone']
    response = requests.post(endpoint_url, headers=headers_missing_timezone, json=payload)
    assert response.status_code in [400, 422], 'Invalid response code'

# Test for empty accept in Header
def test_empty_accept():
    headers_invalid_timezone = headers.copy()
    headers_invalid_timezone['accept'] = ''
    response = requests.post(endpoint_url, headers=headers_invalid_timezone, json=payload)
    assert response.status_code == 422, 'Invalid response code'


# Test for missing accept in Header
def test_missing_accept():
    headers_missing_timezone = headers.copy()
    del headers_missing_timezone['accept']
    response = requests.post(endpoint_url, headers=headers_missing_timezone, json=payload)
    assert response.status_code in [400, 422], 'Invalid response code'


# Test for missing all key expect Authorization Header
def test_missing_all():
    headers_missing_both = headers.copy()
    del headers_missing_both['x-opera-timezone']
    del headers_missing_both['X-Opera-UI-Language']
    del headers_missing_both['accept']
    del headers_missing_both['Content-Type']
    response = requests.post(endpoint_url, headers=headers_missing_both, json=payload)
    assert response.status_code in [400, 422], 'Invalid response code'


# Test with empty header
def test_empty_header():
    response = requests.post(endpoint_url, headers={}, json=payload)
    assert response.status_code == 401, 'Invalid response code'


# Test with invalid Token
def test_invalid_token():
    bearer_token_invalid = 'FAILbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiI5MDU4MjU2MjIiLCJjaWQiOiJvcGVyYV9kZXNrdG9wIiwidmVyIjoiMiIsImlhdCI6IjE3MTA3NzMzNTYiLCJqdGkiOiJCRUloVzg1ZUs0MTcxMDc3Njk1NiJ9.8ZYNJlUvK0hydpo9nODKmSgDzshYPxjPBDKpolr8AI0'
    headers_invalid_token = headers.copy()
    headers_invalid_token['Authorization'] = f'Bearer {bearer_token_invalid}'
    response = requests.post(endpoint_url, headers=headers_invalid_token, json=payload)
    assert response.status_code == 401, 'Invalid response code'


# Test with empty Token
def test_empty_token():
    bearer_token_empty = ''
    headers_empty_token = headers.copy()
    headers_empty_token['Authorization'] = f'Bearer {bearer_token_empty}'
    response = requests.post(endpoint_url, headers=headers_empty_token, json=payload)
    assert response.status_code == 401, 'Invalid response code'


# Test for Invalid Endpoint
def test_invalid_endpoint():
    invalid_endpoint_url = "https://composer.opera-api.com/api/v1/"
    response = requests.post(invalid_endpoint_url, headers=headers, json=payload)
    assert response.status_code in [404, 500, 502, 503], 'Invalid response code'


# Test for check if maximum number of request are handled
def test_max_available_response():
    response_initial = requests.post(endpoint_url, headers=headers, json=payload)
    assert response_initial.status_code == 200, 'Invalid response code'
    assert 'message' in response_initial.json()
    requests_available = response_initial.json().get('requests_available')
    print(f'Request which are able to perform {requests_available}')

    for number in range(requests_available-1):
        payload_continuation = {f'selected_text': f'API Call number {number}'}
        response_continuation = requests.post(endpoint_url, headers=headers, json=payload_continuation)
        assert response_continuation.status_code == 200, 'Invalid response code'
        assert 'message' in response_continuation.json()

    response_final = requests.post(endpoint_url, headers=headers, json=payload)
    assert response_final.status_code == 429, 'Invalid response code'





