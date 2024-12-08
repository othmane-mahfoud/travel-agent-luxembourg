import pandas as pd

if __name__ == "__main__":
    ticketmaster_df = pd.read_csv("data/ticketmaster_events.csv")
    scraping_events = pd.read_csv("data/scraping_events.csv")
    combined_events = pd.concat([ticketmaster_df, scraping_events], ignore_index=True)
    combined_events.to_csv("data/combined_events.csv", index=False)