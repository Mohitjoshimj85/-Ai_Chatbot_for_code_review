import React from 'react';

function ReviewTabs({ review }) {
  let parsedReview = {};

  try {
    // Step 1: If backend wrapped JSON inside a string
    if (typeof review === "string") {
      parsedReview = JSON.parse(review);
    } else if (review && typeof review === "object") {
      // Step 2: Sometimes review itself has a nested string
      parsedReview =
        typeof review.review === "string" ? JSON.parse(review.review) : review;
    }
  } catch (e) {
    parsedReview = { summary: "Could not parse JSON", bugs: "", suggestions: "" };
  }

  return (
    <>
      <ul className="nav nav-tabs mt-4" id="reviewTabs" role="tablist">
        <li className="nav-item" role="presentation">
          <button className="nav-link active" data-bs-toggle="tab" data-bs-target="#summary" type="button">
            Review Summary
          </button>
        </li>
        <li className="nav-item" role="presentation">
          <button className="nav-link" data-bs-toggle="tab" data-bs-target="#bugs" type="button">
            Bugs Found
          </button>
        </li>
        <li className="nav-item" role="presentation">
          <button className="nav-link" data-bs-toggle="tab" data-bs-target="#suggestions" type="button">
            Suggestions
          </button>
        </li>
      </ul>

      <div className="tab-content p-3 border border-top-0" id="reviewTabsContent">
        <div className="tab-pane fade show active" id="summary">
          <pre style={{ whiteSpace: "pre-wrap" }}>{parsedReview.summary || "No summary provided."}</pre>
        </div>
        <div className="tab-pane fade" id="bugs">
          <pre style={{ whiteSpace: "pre-wrap" }}>{parsedReview.bugs || "No bugs found."}</pre>
        </div>
        <div className="tab-pane fade" id="suggestions">
          <pre style={{ whiteSpace: "pre-wrap" }}>{parsedReview.suggestions || "No suggestions available."}</pre>
        </div>
      </div>
    </>
  );
}

export default ReviewTabs;
