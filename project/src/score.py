from .wordemb import WordEmb


def main():
    emb_model = WordEmb()
    emb_model.init()
    print('Emb model ready!')

    q = input('Enter word (or \'q\' to exit): ')
    while q != 'q':
        gender_score, sent_score = emb_model.gender_score(q), emb_model.sent_score(q)
        print('Gender: {}, sent: {}'.format(gender_score, sent_score))
        q = input('Enter word (or \'q\' to exit): ')

if __name__ == '__main__':
    main()
