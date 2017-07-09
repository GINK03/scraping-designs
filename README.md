# itmedia scraper

# What is this.
 これは[itmedia](http://www.itmedia.co.jp/)をスクレイピングをおこなうスクリプトです。  
 簡易的な技術的なコーパスを構築できます　
 
 This is a script that scrapes [itmedia](http://www.itmedia.co.jp/).  
 You can build a simple technical corpus  

# How to use.
git cloneしてお手元のPCにダウンロードします  
git clone and download it to your PC  

```console
$ git clone https://github.com/GINK03/itmedia-scraper
```

requirementsをインストールします  
install requirements.  
```console
$ pip3 install -r requrements.txt
```

実行してダウンロードを開始します  
Run and start downloading
```console
$ python3 scraper.py
```

downloadディレクトリにに各ページが保存されます
Each page is saved in the download directory

```console
@article{ ITmeadi Scraping,
    title   = { ITmedai Scraping },
    author  = { nardtree },
    journal = { arXiv preprint arXiv:1506.06724 },
    year    = { 2017 }
}
```
