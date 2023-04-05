def save_results(results, output_file):
    with open(output_file, "w") as file:
        for result in results:
            file.write(f"{result}\n")