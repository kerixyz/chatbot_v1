# Idea is to call the convo_start function and then put in the blocks 
# for other paths of conversations as other functions that can be called

def convo_start(streamer):
    # Initializations
    convo_paths = {
        'no': convo_no_1,
        'yes': convo_yes_1
    }

    print(f"Hey thanks for watching {streamer} stream. Would you mind ansswering a few questions about your experience?")

    # Store conversation context across conversations
    context = {
        'streamer': streamer
    }

    # Input request
    user_input = input().lower()

    if user_input in convo_paths:
        convo_path = convo_paths[user_input]
        convo_path(context)
        return None

    return None


def convo_no_1(context):
    # No in first prompt
    print("Thank you!")
    return None

def convo_yes_1(context):
    # Yes in first prompt
    print(f"Nice. How was your experience watching {context['streamer']}")
    return None    

if __name__ == '__main__':
    streamer = input().lower()
    convo_start(streamer)