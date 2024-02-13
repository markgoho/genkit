"use strict";

const { getProjectId } = require("@google-genkit/common");
const { configureGenkit } = require("@google-genkit/common/config");
const { setLogLevel } = require("@google-genkit/common/logging");
const { configureVertexAiTextModel } = require("@google-genkit/providers/llms");
const { googleAI, openAI } = require("@google-genkit/providers/models");
const { firestoreStores } = require("@google-genkit/providers/stores");

configureGenkit({
  plugins: [
    firestoreStores({projectId: getProjectId()}),
    googleAI(),
    openAI(),
  ],
  flowstore: "firestoreStores",
  tracestore: "firestoreStores",
  models: [
    configureVertexAiTextModel({ modelName: "gemini-pro" })
  ],
  enableTracingAndMetrics: true,
  logLevel: "info",
})
