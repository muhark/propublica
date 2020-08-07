CREATE TABLE blacklist (
    advertiser VARCHAR(255)
);

INSERT INTO blacklist VALUES ('Penzeys Spices');

SELECT * FROM blacklist;

SELECT * FROM ads
WHERE advertiser IN (
    SELECT advertiser FROM (
        SELECT advertiser, COUNT(*) AS N_ADS FROM ads
        GROUP BY advertiser
        ORDER BY 2 DESC)
    WHERE N_ADS > 100
    AND N_ADS < 700
    AND advertiser IS NOT NULL
    AND advertiser NOT IN (
        SELECT advertiser FROM blacklist
        )
    )
AND political_probability > 0.99
AND listbuilding_fundraising_proba > 0.05 AND listbuilding_fundraising_proba < 0.9
ORDER BY advertiser;

SELECT targetings, targets FROM ads WHERE targetings IS NOT NULL LIMIT 1;