import os
import pandas as pd
import email

# Set folder path and CSV file path
csv_path = "personal_fraud_email.csv"


def email_sorter(folder_path):
    # Load existing data from CSV file into a DataFrame
    if os.path.exists(csv_path):
        data = pd.read_csv(csv_path)
    else:
        data = pd.DataFrame(columns=["Sender", "Raw", "Fraud"])

    # Create a list to hold new DataFrames to be concatenated
    new_dfs = []

    # Loop through files in folder_path
    for filename in os.listdir(folder_path):
        if filename.endswith(".eml"):
            with open(os.path.join(folder_path, filename), "r") as file:
                msg = email.message_from_file(file)
                sender = msg["From"]
                raw_message = str(msg)

                # Check if the data already exists in the DataFrame
                if not (
                    (data["Sender"] == sender) & (data["Raw"] == raw_message)
                ).any():
                    # Create a new DataFrame with the new data
                    new_df = pd.DataFrame(
                        {
                            "Sender": [sender],
                            "Raw": [raw_message],
                            "Fraud": [1 if folder_path == "fraud_emails" else 0],
                        }
                    )

                    # Append the new DataFrame to the list
                    new_dfs.append(new_df)

    # Concatenate the new DataFrames and the existing data into one DataFrame
    if len(new_dfs) > 0:
        data = pd.concat([data] + new_dfs, ignore_index=True)
    return data, filename


# Write the updated data to the CSV file

if __name__ == "__main__":
    # loading fraud emails first
    data, filename = email_sorter("fraud_emails")
    # loading real emails
    data, filename = email_sorter("not_fraud_emails")
    data.to_csv(csv_path, index=False)
    print(f"Length of the personal_fraud_email.csv file: {len(data)}")
    print(f"Number of recorded personal emails: {len(filename)}")
    print("=" * 35 + "Completed" + "=" * 35)
