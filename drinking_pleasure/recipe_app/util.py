import base64


def preprocessing_recipe_data(data):
    data['img'] = base64.decodebytes(data['img']).decode('latin_1')

    for i in range(data['main_meterial_list']):
        img = data['main_meterial_list'][i]['img']
        data['main_meterial_list'][i]['img'] = base64.decodebytes(img).decode('latin_1')

    for i in range(data['sub_meterial_list']):
        img = data['sub_meterial_list'][i]['img']
        data['sub_meterial_list'][i]['img'] = base64.decodebytes(img).decode('latin_1')

    return data


def preprocessing_list_data(data):
    for i in range(data):
        img = data['img']
        data[i]['img'] = base64.decodebytes(img).decode('latin_1')

    return data
