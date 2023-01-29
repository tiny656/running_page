python3 scripts/joyrun_sync.py ${your mobile} ${your 验证码} --with-gpx

python3 scripts/gen_svg.py --from-db --title "my running page" --type grid --athlete "RealTiny656" --output assets/grid.svg --min-distance 10.0 --special-color yellow --special-color2 red --special-distance 20 --special-distance2 40 --use-localtime

python3 scripts/gen_svg.py --from-db --title "my running page" --type github --athlete "RealTiny656" --special-distance 10  --special-distance2 20 --special-color yellow --special-color2 red --output assets/github.svg --use-localtime --min-distance 0.5

python3 scripts/gen_svg.py --from-db --type circular --use-localtime

yarn build-prefix

cp -r /root/running_page/public/. /root/running_page/gh-pages/
cp -r /root/running_page/assets /root/running_page/gh-pages/assets
