// Copyright 2025 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
// SPDX-License-Identifier: Apache-2.0

package snippets

import (
	"context"
	"log"

	"github.com/firebase/genkit/go/ai"
	"github.com/firebase/genkit/go/genkit"
	"github.com/firebase/genkit/go/plugins/googleai"
)

func googleaiEx(ctx context.Context) error {
	g, err := genkit.Init(ctx)
	if err != nil {
		log.Fatal(err)
	}

	// [START init]
	if err := googleai.Init(ctx, g, nil); err != nil {
		return err
	}
	// [END init]

	yourKey := ""
	// [START initkey]
	if err := googleai.Init(ctx, g, &googleai.Config{APIKey: yourKey}); err != nil {
		return err
	}
	// [END initkey]

	// [START model]
	model := googleai.Model(g, "gemini-1.5-flash")
	// [END model]

	// [START gen]
	text, err := genkit.GenerateText(ctx, g, ai.WithModel(model), ai.WithPromptText("Tell me a joke."))
	if err != nil {
		return err
	}
	// [END gen]

	_ = text

	var userInput string

	// [START embedder]
	embeddingModel := googleai.Embedder(g, "text-embedding-004")
	// [END embedder]

	// [START embed]
	embedRes, err := ai.Embed(ctx, embeddingModel, ai.WithEmbedText(userInput))
	if err != nil {
		return err
	}
	// [END embed]

	_ = embedRes

	var myRetriever ai.Retriever

	// [START retrieve]
	retrieveRes, err := ai.Retrieve(ctx, myRetriever, ai.WithRetrieverText(userInput))
	if err != nil {
		return err
	}
	// [END retrieve]

	_ = retrieveRes

	var myIndexer ai.Indexer
	var docsToIndex []*ai.Document

	// [START index]
	if err := ai.Index(ctx, myIndexer, ai.WithIndexerDocs(docsToIndex...)); err != nil {
		return err
	}
	// [END index]

	return nil
}
