import numpy as np
# import tensorflow as tf
import tensorflow_hub as hub
from sklearn.metrics.pairwise import cosine_similarity
import tensorflow.compat.v1 as tf

tf.compat.v1.disable_eager_execution()


class sentence_similarity:
    def __init__(self):
        self.module_url = "https://tfhub.dev/google/universal-sentence-encoder/2"
        self.threshold = 0.6

    # get cosine similairty matrix
    def cos_sim(self, input_vectors):
        similarity = cosine_similarity(input_vectors)
        return similarity

    # get topN similar sentences
    def get_top_similar(self, s, sentence_list, similarity_matrix, N):
        # find the index of sentence in list
        index = sentence_list.index(s)
        # get the corresponding row in similarity matrix
        similarity_row = np.array(similarity_matrix[index, :])
        # get the indices of top similar
        sorted_arr = np. sort(similarity_row[:-1])
        indices = similarity_row[:-1].argsort()
        return [sentence_list[i] for i in indices], sorted_arr

    def _run(self, sentences_list, sentence):
        # Import the Universal Sentence Encoder's TF Hub module
        embed = hub.Module(self.module_url)
        # Reduce logging output.
        tf.logging.set_verbosity(tf.logging.ERROR)
        if sentence not in sentences_list:
            sentences_list.append(sentence)
        with tf.Session() as session:
            session.run([tf.global_variables_initializer(), tf.tables_initializer()])
            sentences_embeddings = session.run(embed(sentences_list))

        similarity_matrix = self.cos_sim(np.array(sentences_embeddings))
        top_similar, val = self.get_top_similar(sentence, sentences_list, similarity_matrix, 3)
        print(top_similar)
        if val[-1] > self.threshold:
            return (True, top_similar[-1], val[-1])
        else:
            return (False, top_similar[-1], val[-1])


if __name__ == '__main__':
    sample_sentences_list = ["you are mean", "I hate you", "I love ramen"]
    sample_sentence = "Hi"
    ss = sentence_similarity()
    present = ss._run(sample_sentences_list, sample_sentence)
    print(present)

