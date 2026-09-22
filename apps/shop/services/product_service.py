def soft_delete_product(product):
    product.soft_delete()
    return True


def restore_product(product):
    product.restore()
    return True
