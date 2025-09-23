from flappybird.src.levels.level_manager_instance import level_manager

def main():
    level_manager.load_level()
    # Spiel starten
    level_manager.start_game()

if __name__ == "__main__":
    main()
