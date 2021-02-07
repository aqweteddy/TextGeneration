python train_script.py --model_type rag \
--train_data data/pig/rss.json \
--max_len 300 \
--batch_size 4 \
--num_workers 15 \
--lr 2e-5 --gpus 1 \
--max_epochs 3 \
--save_top_k 6 \
--wiki_ds_path rag_ckpt/wiki_tw_index/wiki_tw_dataset \
--wiki_index_path rag_ckpt/wiki_tw_index/wiki_tw_hnsw_index.faiss \
--rag_ckpt_path rag_ckpt/rag_init
