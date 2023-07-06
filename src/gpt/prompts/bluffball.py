prompt = """
Your task is to generate a short water cooler style conversation about a specific piece football news in a mild cockney accent.

Here are the rules, which you must follow at all costs.
The two characters are surly middle aged men, labelled "Bluffball" and "You". This labelling appears only at the start of each line.
You must alternate between "Bluffball:" and "You:" to start each line. Do not use either word anywhere else in the conversation.
Neither character ever says the word "Bluffball". 
The word Bluffball can only appear after a newline to introduce the speaker.
They both know exactly what happened in the football news. They never admit that they don't know an item of news.
They talk specifically about the news, and they don't stray onto talking about football more generally.
They both have a great deal of expertise about football.
They enjoy complaining about football but they do not admit it. In fact, they do not ever speak positively about football news, only negatively.
They never ask each other a question that suggests they don't know something. 
They never address one another by name. 
The conversation will start with the phrase "You: Did you see that ludicrous display last night?".
You will receive some football news in JSON format.

Here is an example:
You: Did you see that ludicrous display last night?
Bluffball: What was Wenger thinking sending Walcott on that early?
You: The thing about Arsenal is, they always try and walk it in.
Bluffball: That's true.
You: Mind how you go.

Here is another example:
You: Did you see that ludicrous display last night?
Bluffball: How could Chelsea let Mount go to Man U?
You: The thing about Chelsea is, they're spoilt for expensive players.
Bluffball: That's true.
You: Mind how you go.

Here is your news:
"""