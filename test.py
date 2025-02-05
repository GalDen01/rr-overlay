from scraper import get_rating_and_rank

player = "luciee"
rating, rank = get_rating_and_rank(player)
print(f"MMR: {rating}, Rank: {rank}")