def generate_report(data):
    with open('intrusion_report.txt', 'w') as report:
        report.write("Intrusion Report\n")
        report.write("================\n")
        report.write(data)

if __name__ == "__main__":
    # Example Usage
    generate_report("Details of detected intrusion.")