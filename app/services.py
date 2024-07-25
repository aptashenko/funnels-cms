def get_random_promocode():
    promocodes = Promocodes.query.filter_by(user_email=None).all()
    print(len(promocodes))
    promocode = random.choice(promocodes)
    return promocode.value