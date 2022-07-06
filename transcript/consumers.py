import riva_api.riva_audio_pb2 as ra
import riva_api.riva_asr_pb2_grpc as rasr_srv
import riva_api.riva_asr_pb2 as rasr
import grpc
from channels.generic.websocket import WebsocketConsumer
from dotenv import load_dotenv
import os

# from transcribe_file import CHUNK
CHUNK = 1024
load_dotenv()
# Instantiates a client
channel = grpc.insecure_channel(
    os.environ['TRANSCRIBE_API_BASE'])
client = rasr_srv.RivaSpeechRecognitionStub(channel)
config = rasr.RecognitionConfig(
    encoding=ra.AudioEncoding.LINEAR_PCM,
    sample_rate_hertz=16000,
    language_code='en-US',
    max_alternatives=1,
    enable_automatic_punctuation=True,
)

streaming_config = rasr.StreamingRecognitionConfig(
    config=config, interim_results=True)


class TranscriptConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def process(self, responses):
        # TODO: Currently its printing responses. We need to send back to socket
        num_chars_printed = 0

        for response in responses:
            if not response.results:
                continue

            partial_transcript = ""
            for result in response.results:
                if not result.alternatives:
                    continue

                transcript = result.alternatives[0].transcript

                if not result.is_final:
                    partial_transcript += transcript
                else:
                    overwrite_chars = ' ' * \
                        (num_chars_printed - len(transcript))

                    # TODO: To sendback uncomment following line
                    print(text_data=transcript + overwrite_chars)
                    # self.send(text_data=transcript + overwrite_chars)

                    num_chars_printed = 0

            if partial_transcript != "":
                num_chars_printed = len(partial_transcript)

    def receive(self, text_data=None, bytes_data=None):

        if bytes_data:
            print(bytes_data)

            # NOT WORKING TRY - Test with decoding with base64 decode
            # print(base64.b64decode(bytes_data))
            # opus_data = BytesIO(bytes_data)
            # sound = AudioSegment.from_file(opus_data, codec="opus")
            # play(sound)
            # file_in_memory = io.BytesIO(bytes_data)
            # file_in_memory.seek(0)
            # wf = wave.open(file_in_memory, 'rb')
            # def generator(w, s):
            #     yield rasr.StreamingRecognizeRequest(streaming_config=s)
            #     d = w.readframes(CHUNK)
            #     while len(d) > 0:
            #         yield rasr.StreamingRecognizeRequest(audio_content=d)
            #         d = w.readframes(CHUNK)

            # responses = client.StreamingRecognize(
            #     generator(wf, streaming_config))
            # self.process(responses)

            # WORKING one for Transcribing local wav file as streaming request to ASR
            # wf = wave.open('/Users/umesh/Desktop/big_bang_cut.wav', 'rb')
            # def generator(w, s):
            #     yield rasr.StreamingRecognizeRequest(streaming_config=s)
            #     d = w.readframes(CHUNK)
            #     while len(d) > 0:
            #         yield rasr.StreamingRecognizeRequest(audio_content=d)
            #         d = w.readframes(CHUNK)

            # responses = client.StreamingRecognize(
            #     generator(wf, streaming_config))
            # self.process(responses)

            # NOT WORKING TRY - Sending bytes array directly assuming coming req is WAV
            # requests = (rasr.StreamingRecognizeRequest(audio_content=content)
            #             for content in [bytes_data])
            # def build_generator(cfg, gen):
            #     yield rasr.StreamingRecognizeRequest(streaming_config=cfg)
            #     for x in gen:
            #         yield x

            # responses = client.StreamingRecognize(
            #     build_generator(streaming_config, requests))
            # self.process(responses)
