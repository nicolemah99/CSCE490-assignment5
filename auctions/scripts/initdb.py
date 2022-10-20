import csv
from auctions.models import *

FNAME = "auctions/seeddata/listings.csv"

def run():
    print(f'Reading file: {FNAME}')
    with open(FNAME) as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(f'Processsing: {row}')
            name = row["name"]
            currentBid = row["currentBid"]
            description = row["description"]
            user = row["user"]
            category = row["category"]
            datePosted =row["datePosted"]
            dateBidEnd =row["dateBidEnd"]
            image=row["image"]

            Listing.objects.get_or_create(name=name, currentBid=currentBid, description=description, user=user, category=category, datePosted =datePosted,dateBidEnd=dateBidEnd, image=image)

