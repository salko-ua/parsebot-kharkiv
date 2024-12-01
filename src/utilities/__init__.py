
async def check_is_exist_name_to_delete(text: str, name_to_delete: str) -> str:
    all_names = text.split()
    result = False
    for name in all_names:
        if name == name_to_delete:
            result = True
    return result

async def delete_exist_name_in_str(text: str, name_to_delete: str) -> str:
        all_names = text.split()
        for name in all_names:
            if name == name_to_delete:
                all_names.remove(name)
        return " ".join(all_names)