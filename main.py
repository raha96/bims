import qrcode
img = qrcode.make('data')
img.save('currentqr.png')
