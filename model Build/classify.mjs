// classify.mjs
// Run with: node classify.mjs

import fs from "fs";
import { execSync } from "child_process";

const inputFile = "toExtractContext.json";
const outputFile = "toExtractContextOutput.json";

console.log("🔍 Watching for input file...");

function checkAndProcessFile() {
  if (fs.existsSync(inputFile)) {
    try {
      console.log(`📥 Found ${inputFile}, reading...`);

      // Step 1: Read input JSON
      const rawData = fs.readFileSync(inputFile, "utf8").trim();
      if (!rawData) {
        console.log("⚠️ INVALID DATA: File is empty. Waiting for data...");
        return;
      }

      let inputData;
      try {
        inputData = JSON.parse(rawData);
      } catch (e) {
        console.log("⚠️ INVALID DATA: JSON not valid. Waiting for correction...");
        return;
      }

      const subject = (inputData.subject || "").trim();
      const body = (inputData.body || "").trim();

      if (!subject && !body) {
        console.log("⚠️ INVALID DATA: Missing subject & body. Waiting for update...");
        return;
      }

      // Step 2: Run Python model
      const command = `python predict.py "${subject}" "${body}"`;
      const result = execSync(command).toString().trim();

      // Step 3: Parse Python output JSON
      const parsedResult = JSON.parse(result);

      // Step 4: Save result to output file
      fs.writeFileSync(outputFile, JSON.stringify(parsedResult, null, 2), "utf8");

      // Step 5: Print result in terminal
      console.log("✅ Prediction Result:", parsedResult);

      // Step 6: Remove input file only after valid processing
      fs.unlinkSync(inputFile);
      console.log(`🗑️ Deleted ${inputFile}, waiting for next file...`);

    } catch (error) {
      console.error("❌ Error processing file:", error.message);
    }
  }
}

// Check every 1 second
setInterval(checkAndProcessFile, 1000);
