import csv
from datetime import datetime

partner_config = {
    "ACME": {
        "file": "acme.txt",
        "delimiter": "|",
        "partner_code": "ACME",
        "columns": {
            "MBI": "external_id",
            "FNAME": "first_name",
            "LNAME": "last_name",
            "DOB": "dob",
            "EMAIL": "email",
            "PHONE": "phone"
        }
    },
    "BETTERCARE": {
        "file": "bettercare.csv",
        "delimiter": ",",
        "partner_code": "BETTERCARE",
        "columns": {
            "subscriber_id": "external_id",
            "first_name": "first_name",
            "last_name": "last_name",
            "date_of_birth": "dob",
            "email": "email",
            "phone": "phone"
        }
    }
}

def format_phone(phone):
    digits = "".join(c for c in phone if c.isdigit())
    return f"{digits[0:3]}-{digits[3:6]}-{digits[6:10]}"

def format_dob(dob):
    try:
        if "/" in dob:
            return datetime.strptime(dob, "%m/%d/%Y").strftime("%Y-%m-%d")
        return datetime.strptime(dob, "%Y-%m-%d").strftime("%Y-%m-%d")
    except:
        return None

def process_partner(partner_name, config):
    results = []
    with open(config["file"], newline="") as f:
        reader = csv.DictReader(f, delimiter=config["delimiter"])
        for row in reader:
            record = {"partner_code": config["partner_code"]}

            for source_col, target_col in config["columns"].items():
                value = row.get(source_col, "").strip()
                record[target_col] = value

            if not record["external_id"]:
                continue  # validation

            record["first_name"] = record["first_name"].title()
            record["last_name"] = record["last_name"].title()
            record["email"] = record["email"].lower()
            record["dob"] = format_dob(record["dob"])
            record["phone"] = format_phone(record["phone"])

            results.append(record)

    return results

def main():
    all_data = []
    for partner, config in partner_config.items():
        data = process_partner(partner, config)
        all_data.extend(data)

    for row in all_data:
        print(row)

if __name__ == "__main__":
    main()
