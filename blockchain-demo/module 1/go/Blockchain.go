package main

import (
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"time"
)

type Block struct {
	Index        int
	Timestamp    string
	Nonce        int
	Data         string
	PreviousHash string
	Hash         string
}

func newBlock(index int, nonce int, data string, previousHash string) *Block {
	block := Block{
		Index:        index,
		Timestamp:    time.Now().Format(time.RFC3339),
		Nonce:        nonce,
		Data:         data,
		PreviousHash: previousHash,
	}
	block.Hash = block.ToHash()
	return &block
}

func (b *Block) PlusNonce() {
	b.Nonce++
	b.Hash = b.ToHash()
}

func (b *Block) ToHash() string {
	blockBytes, _ := json.Marshal(b)
	hash := sha256.Sum256(blockBytes)
	return hex.EncodeToString(hash[:])
}

type Blockchain struct {
	Blocks []*Block
}

func NewBlockchain() *Blockchain {
	return &Blockchain{
		Blocks: []*Block{newBlock(0, 0, "Genesis Block", "0")},
	}
}

func (bc *Blockchain) AddBlock(data string) {
	previousBlock := bc.Blocks[len(bc.Blocks)-1]
	newBlock := newBlock(len(bc.Blocks), 0, data, previousBlock.Hash)
	ProofOfWork(newBlock, 4)
	bc.Blocks = append(bc.Blocks, newBlock)
}

func ProofOfWork(block *Block, difficulty int) {
	prefix := ""
	for i := 0; i < difficulty; i++ {
		prefix += "0"
	}
	for {
		hash := block.Hash
		if hash[:difficulty] == prefix {
			break
		}
		block.PlusNonce()
	}
}

func main() {
	blockchain := NewBlockchain()
	blockchain.AddBlock("First Block Data")
	blockchain.AddBlock("Second Block Data")
	blockchain.AddBlock("Third Block Data")

	for _, block := range blockchain.Blocks {
		blockJSON, _ := json.MarshalIndent(block, "", "  ")
		println(string(blockJSON))
	}
}
