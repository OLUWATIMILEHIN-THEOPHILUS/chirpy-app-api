from rest_framework import serializers
from chirps.models import Chirp, ChirpMedia, ChirpComment, ChirpLike

class ChirpMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChirpMedia
        fields = ['media', 'caption']

class ChirpSerializer(serializers.ModelSerializer):
    text = serializers.CharField(max_length=500)

    media = ChirpMediaSerializer(many=True, required=False, read_only=True)
    caption = ChirpMediaSerializer(many=True, required=False, read_only=True)

    uploaded_media = serializers.ListField(
        child = serializers.FileField(max_length=1000000, allow_empty_file=True, use_url=False), write_only=True, required=False
    ) 
    uploaded_caption = serializers.ListField(
        child = serializers.CharField(max_length=100), write_only=True, required=False
    )
    class Meta:
        model = Chirp
        fields = ['text', 'media', 'caption', 'uploaded_media', 'uploaded_caption']

    def create(self, validated_data):
        uploaded_media = validated_data.pop("uploaded_media", [])
        uploaded_caption = validated_data.pop("uploaded_caption", [])

        chirp = Chirp.objects.create(**validated_data)

        for media, caption in zip(uploaded_media, uploaded_caption):
            data = [media, caption]
            media_data = data[0]
            caption_data = data[1]

            ChirpMedia.objects.create(chirp=chirp, media=media_data, caption=caption_data)
        return chirp

class ChirpCommentSerializer(serializers.ModelSerializer):
    text = serializers.CharField(max_length=500)
    class Meta:
        model = ChirpComment
        fields = ['text']

class ChirpLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChirpLike
        fields = ['uid']
