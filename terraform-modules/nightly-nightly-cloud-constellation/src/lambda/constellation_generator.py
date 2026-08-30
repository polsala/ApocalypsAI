import random
import json

def lambda_handler(event, context):
    constellations = [
        """
        ✨  The Cosmic Dust Bunny  ✨
             *       .
                   *
           .   _/\_   .
              /____\\
             /      \\
            /________\\
           /__________\\
          /____________\\
         /______________\\
        /________________\\
       /__________________\\
      /____________________\\
     /______________________\\
    /________________________\\
   /__________________________\\
  /____________________________\\
 /______________________________\\
/________________________________\\
        """,
        """
        🌌  The Wandering Starfish  🌌
              *   *
             / \\ / \\
            |   X   |
             \\ / \\ /
              *   *
        """,
        """
        🌠  The Galactic Gherkin  🌠
              _.-'-._
             /       \\
            |  🥒🥒  |
             \\       /
              '-._.-'
        """,
        """
        💫  The Nebulous Noodle  💫
           ~ ~ ~ ~ ~
          ~         ~
         ~           ~
        ~             ~
         ~           ~
          ~         ~
           ~ ~ ~ ~ ~
        """,
        """
        🌟  The Celestial Teacup  🌟
             ( )
            /   \\
           |     |
           \\_____/
        """,
        """
        ✨  A message from the void: You are doing great!  ✨
        """
    ]

    chosen_constellation = random.choice(constellations)

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': chosen_constellation
    }
