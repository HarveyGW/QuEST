# File: main_analysis.py

from encryption_protocols import rsa_encryption, bb84, e91
import pandas as pd
import matplotlib.pyplot as plt


def run_experiments(n=20):
    rsa_times = []
    bb84_times = []
    e91_times = []

    for _ in range(n):
        gen_time = rsa_encryption()
        rsa_times.append(gen_time)

        bb84_time = bb84()
        bb84_times.append(bb84_time)

        e91_time = e91()
        e91_times.append(e91_time)

    data = {
        "RSA Time": rsa_times,
        "BB84 Time": bb84_times,
        "E91 Time": e91_times,
    }
    df = pd.DataFrame(data)
    df.to_csv("encryption_performance.csv", index=False)
    print("Data collected and stored in encryption_performance.csv")


def plot():
    df = pd.read_csv("encryption_performance.csv")

    # Focus on numeric columns for execution times
    numeric_columns = [
        "RSA Time",
        "BB84 Time",
        "E91 Time",
    ]
    numeric_df = df[numeric_columns].apply(pd.to_numeric, errors="coerce")

    # Calculate average times for numeric data
    avg_times = numeric_df.mean()

    # Plotting average execution times with a line chart
    plt.figure(figsize=(10, 7))
    avg_times.plot(kind="line", marker="o")
    plt.title("Average Execution Times for Encryption Protocols")
    plt.ylabel("Time (seconds)")
    plt.xlabel("Protocols")
    plt.grid(True)
    plt.xticks(
        ticks=range(len(numeric_columns)),
        labels=numeric_columns,
        rotation=45,
        ha="right",
    )
    plt.tight_layout()
    plt.savefig(
        "protocol_times_line_chart.png"
    )
    plt.show()


if __name__ == "__main__":
    run_experiments(20)
    plot()
