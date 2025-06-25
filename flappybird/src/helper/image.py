import pygame


def rotate_and_keep_size(image: pygame.Surface, angle:float) -> pygame.Surface:
    # 1. Rotieren ohne Antialiasing
    rotated = pygame.transform.rotate(image, angle)

    # 2. Auf Originalgröße zuschneiden (NES-Stil: keine Vergrößerung!)
    rotated_rect = rotated.get_rect()
    crop_rect = pygame.Rect(
        (rotated_rect.width - image.get_width()) // 2,
        (rotated_rect.height - image.get_height()) // 2,
        image.get_width(),
        image.get_height())
    return rotated.subsurface(crop_rect).copy()
