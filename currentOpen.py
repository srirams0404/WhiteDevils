import psutil

def categorize_processes():
    processes = psutil.process_iter(['pid', 'name', 'status'])

    categories = {
        'entertainment': [],
        'studying': []
    }

    for process in processes:
        pid, name, status = process.info['pid'], process.info['name'], process.info['status']

        if "vlc" in name.lower():
            categories['entertainment'].append((pid, name))
        elif "pycharm" in name.lower() or "acrobat" in name.lower():
            categories['studying'].append((pid, name))

    return categories

if __name__ == "__main__":
    process_categories = categorize_processes()

    for category, processes in process_categories.items():
        print(f"{category.capitalize()} processes:")
        for pid, name in processes:
            print(f"  PID: {pid}, Name: {name}")
        print()