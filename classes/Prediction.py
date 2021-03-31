import classes.BoundingBox as BoundingBox
import dash_html_components as html

LABELS = {0.0: 'birdCall',
          1.0: 'blueSunglasses',
          2.0: 'brownDie',
          3.0: 'cactusPaper',
          4.0: 'canadaPencil',
          5.0: 'carabiner',
          6.0: 'cloudSign',
          7.0: 'cowbell',
          8.0: 'cupcakePaper',
          9.0: 'eyeball',
          10.0: 'foamDart',
          11.0: 'gClamp',
          12.0: 'giftBag',
          13.0: 'glassBead',
          14.0: 'gyroscope',
          15.0: 'hairClip',
          16.0: 'hairRoller',
          17.0: 'lavenderDie',
          18.0: 'legoBracelet',
          19.0: 'metalKey',
          20.0: 'miniCards',
          21.0: 'noisemaker',
          22.0: 'paperPlate',
          23.0: 'partyFavor',
          24.0: 'pinkCandle',
          25.0: 'pinkEraser',
          26.0: 'plaidPencil',
          27.0: 'pumpkinNotes',
          28.0: 'rainbowPens',
          29.0: 'redBow',
          30.0: 'redDart',
          31.0: 'redWhistle',
          32.0: 'rubiksCube',
          33.0: 'sign',
          34.0: 'silverStraw',
          35.0: 'spiderRing',
          36.0: 'stickerBox',
          37.0: 'trophy',
          38.0: 'turtle',
          39.0: 'vancouverCards',
          40.0: 'voiceRecorder',
          41.0: 'yellowBag',
          42.0: 'yellowBalloon',
          43.0: 'Invalid label'}


class Prediction:
    def __init__(self, label, score, bounding_box):
        if isinstance(label, str):
            self.label = label
        else:
            self.label = LABELS[label]

        self.score = score
        self.bounding_box = bounding_box

    def __str__(self):
        return f"Label: {self.label}, score: {self.score}, relative bounding box: {self.bounding_box.__str__()}"

    def toHTML(self):
        b, g, r = self.bounding_box.color
        return f'<a style="color: rgb({r}, {g}, {b});">' + f"Label: {self.label} " \
               + f"</a>, score: {self.score}, relative bounding box: {self.bounding_box.__str__()}"

    def toHTMLDash(self):
        b, g, r = self.bounding_box.color
        return html.P(children=[html.Div(children=f"Label: {self.label} ", style={"color": f"rgb({r}, {g}, {b})"}),
                html.Div(children=f"score: {self.score}, relative bounding box: {self.bounding_box.__str__()}")])
