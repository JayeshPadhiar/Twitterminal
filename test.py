def test(*args):
    if len(args) == 0:
        print('yes', args)
    else:
        print('No', args)

test(1)